"""從古騰堡計畫下載公版電子書，放進 GitHub Pages 的書架（docs/books）。

每本書可以列好幾個古騰堡編號，依序嘗試；下載後會檢查 epub 裡的書名，
對不上就跳過，避免放錯書。由 GitHub Actions 執行（.github/workflows/fetch-books.yml）。
"""
import io
import json
import os
import re
import sys
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


def main():
    books = json.load(open(os.path.join(ROOT, 'scripts', 'books.json'), encoding='utf-8'))
    os.makedirs(OUT, exist_ok=True)
    shelf = []
    for b in books:
        saved = False
        for gid in b['gutenberg']:
            for url in (f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}-images.epub',
                        f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.epub'):
                try:
                    data = get(url)
                    title = epub_title(data)
                except Exception as e:  # noqa: BLE001
                    print(f'  {b["id"]}: {url} failed: {e}')
                    continue
                print(f'  {b["id"]}: #{gid} title={title!r} size={len(data)}')
                if b['expect'] not in title:
                    print(f'  {b["id"]}: title does not match {b["expect"]!r}, skipped')
                    break
                with open(os.path.join(OUT, b['id'] + '.epub'), 'wb') as f:
                    f.write(data)
                shelf.append({'id': b['id'], 'title': b['title'], 'author': b['author'], 'lang': b['lang'],
                              'file': b['id'] + '.epub', 'source': f'https://www.gutenberg.org/ebooks/{gid}'})
                saved = True
                break
            if saved:
                break
        if not saved:
            print(f'!! {b["id"]}: no matching download')
    with open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump({'books': shelf}, f, ensure_ascii=False, indent=2)
    print(f'saved {len(shelf)} of {len(books)} books')
    return 0 if shelf else 1


if __name__ == '__main__':
    sys.exit(main())
