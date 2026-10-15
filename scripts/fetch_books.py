"""從古騰堡計畫下載公版電子書，放進 GitHub Pages 的書架（docs/books）。

每本書可以列好幾個古騰堡編號，依序嘗試；下載後會檢查 epub 裡的書名，
對不上就跳過，避免放錯書。由 GitHub Actions 執行（.github/workflows/fetch-books.yml）。
"""
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs', 'books')
UA = {'User-Agent': 'scroll-reader-bookshelf/1.0 (GitHub Actions)'}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def epub_title(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    container = z.read('META-INF/container.xml').decode('utf-8', 'replace')
    opf_path = re.search(r'full-path="([^"]+)"', container).group(1)
    opf = z.read(opf_path).decode('utf-8', 'replace')
    m = re.search(r'<dc:title[^>]*>(.*?)</dc:title>', opf, re.S)
    return m.group(1).strip() if m else ''


def title_ok(b, title):
    return b['expect'] in title and not any(x in title for x in b.get('exclude', []))


def shrink(data):
    """插畫版 epub 太大時，把大圖縮到長邊 800px、JPEG 品質 60，讓手機打開快一點。"""
    if len(data) < 3_000_000:
        return data
    try:
        from PIL import Image
    except ImportError:
        return data
    src = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    dst = zipfile.ZipFile(out, 'w')
    for info in src.infolist():
        raw = src.read(info.filename)
        low = info.filename.lower()
        if len(raw) > 40_000 and low.endswith(('.jpg', '.jpeg', '.png')):
            try:
                im = Image.open(io.BytesIO(raw))
                im.thumbnail((800, 800))
                buf = io.BytesIO()
                if low.endswith('.png'):
                    # 插圖多半是線稿，減成 64 色的 PNG 就看不出差別，但檔案小很多
                    if im.mode not in ('P', 'L', '1'):
                        im = im.convert('RGB').quantize(64)
                    im.save(buf, 'PNG', optimize=True)
                else:
                    im.convert('RGB').save(buf, 'JPEG', quality=60, optimize=True)
                if buf.tell() < len(raw):
                    raw = buf.getvalue()
            except Exception as e:  # noqa: BLE001
                print(f'    keep {info.filename}: {e}')
        kind = zipfile.ZIP_STORED if info.filename == 'mimetype' else zipfile.ZIP_DEFLATED
        dst.writestr(info.filename, raw, compress_type=kind)
    dst.close()
    print(f'    shrunk {len(data)} -> {out.tell()} bytes')
    return out.getvalue()


def search_ids(b):
    """用 Gutendex（古騰堡書目的公開搜尋服務）找書號，回傳書名符合的前幾筆。"""
    q = urllib.parse.quote(b.get('search') or b['title'])
    data = None
    for _ in range(2):
        try:
            data = json.loads(get(f'https://gutendex.com/books/?search={q}&languages={b["lang"]}'))
            break
        except Exception as e:  # noqa: BLE001
            print(f'  {b["id"]}: search failed: {e}')
    if data is None:
        return []
    ids = [r['id'] for r in data.get('results', []) if title_ok(b, r.get('title', ''))]
    print(f'  {b["id"]}: search {b.get("search") or b["title"]!r} -> {ids[:5]}')
    return ids[:5]


def main():
    books = json.load(open(os.path.join(ROOT, 'scripts', 'books.json'), encoding='utf-8'))
    os.makedirs(OUT, exist_ok=True)
    shelf = []
    for b in books:
        saved = False
        ids = list(b.get('gutenberg', []))
        if not ids:
            ids = search_ids(b)
        for gid in ids:
            for url in (f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}-images.epub',
                        f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.epub'):
                try:
                    data = get(url)
                    title = epub_title(data)
                except Exception as e:  # noqa: BLE001
                    print(f'  {b["id"]}: {url} failed: {e}')
                    continue
                print(f'  {b["id"]}: #{gid} title={title!r} size={len(data)}')
                if not title_ok(b, title):
                    print(f'  {b["id"]}: title does not match {b["expect"]!r}, skipped')
                    break
                small = shrink(data)
                if len(small) > 12_000_000 and '-images' in url:
                    print(f'  {b["id"]}: still {len(small)} bytes with pictures, using the text-only edition')
                    continue
                with open(os.path.join(OUT, b['id'] + '.epub'), 'wb') as f:
                    f.write(small)
                shelf.append({'id': b['id'], 'title': b['title'], 'author': b['author'], 'lang': b['lang'],
                              'file': b['id'] + '.epub', 'source': f'https://www.gutenberg.org/ebooks/{gid}'})
                saved = True
                break
            if saved:
                break
        if not saved and b.get('gutenberg'):
            for gid in search_ids(b):   # 書號不對時改用搜尋
                if gid in b['gutenberg']:
                    continue
                try:
                    data = get(f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}-images.epub')
                    title = epub_title(data)
                except Exception as e:  # noqa: BLE001
                    print(f'  {b["id"]}: #{gid} failed: {e}')
                    continue
                if title_ok(b, title):
                    with open(os.path.join(OUT, b['id'] + '.epub'), 'wb') as f:
                        f.write(shrink(data))
                    shelf.append({'id': b['id'], 'title': b['title'], 'author': b['author'], 'lang': b['lang'],
                                  'file': b['id'] + '.epub', 'source': f'https://www.gutenberg.org/ebooks/{gid}'})
                    saved = True
                    print(f'  {b["id"]}: found by search #{gid}')
                    break
        if not saved:
            print(f'!! {b["id"]}: no matching download')
            old = os.path.join(OUT, b['id'] + '.epub')
            if os.path.exists(old):
                os.remove(old)
    with open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump({'books': shelf}, f, ensure_ascii=False, indent=2)
    print(f'saved {len(shelf)} of {len(books)} books')
    return 0 if shelf else 1


if __name__ == '__main__':
    sys.exit(main())
