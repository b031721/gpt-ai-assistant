"""把公版聖經經文轉成「聖經學英文」頁面用的小檔案（每章一個 JSON）。

來源：https://github.com/scrollmapper/bible_databases （formats/json）
  BSB   Berean Standard Bible，2023 年起捐為公有領域，現代英文
  BBE   Bible in Basic English（1949/1964），只用約一千個基本單字
  ChiUn 和合本（1919，繁體），公有領域

用法：python3 scripts/build_bible.py <放 BSB.json、BBE.json、ChiUn.json 的資料夾>
"""
import json
import os
import re
import sys

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'bible', 'data')
os.makedirs(OUT, exist_ok=True)

V = {v: json.load(open(os.path.join(SRC, v + '.json'), encoding='utf-8'))['books'] for v in ('BSB', 'BBE', 'ChiUn')}
CJK = r'[　-〿一-鿿＀-￯「」『』]'


def zh(t):
    # 原始資料在詞與詞之間有空格，中文不需要
    return re.sub(r'\s+', '', t).strip()


def en(t):
    return re.sub(r'\s+', ' ', t).strip()


counts = []
for bi, book in enumerate(V['BSB']):
    counts.append(len(book['chapters']))
    for ci in range(len(book['chapters'])):
        rows = {}
        for key, fix in (('BSB', en), ('BBE', en), ('ChiUn', zh)):
            chs = V[key][bi]['chapters']
            if ci >= len(chs):
                continue
            for v in chs[ci]['verses']:
                rows.setdefault(v['verse'], {})[key] = fix(v['text'])
        data = [[n, r.get('BSB', ''), r.get('BBE', ''), r.get('ChiUn', '')] for n, r in sorted(rows.items())]
        with open(os.path.join(OUT, f'{bi + 1}-{ci + 1}.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
print('books', len(counts), 'chapters', sum(counts))
print(json.dumps(counts))
