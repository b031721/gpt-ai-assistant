// 下載《動物農莊》(George Orwell, 1945) 英文原文，存成線上閱讀器使用的純文字檔。
// 來源：Project Gutenberg Australia（作者 1950 年過世，在台灣、澳洲、歐盟等地已屬公有領域；
// 美國著作權至 2041 年才到期，請依你所在地法律使用）。
//
// 用法：node scripts/fetch-animal-farm.mjs
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const SOURCE = 'https://gutenberg.net.au/ebooks01/0100011h.html';
const OUT = fileURLToPath(new URL('../public/reader/books/animal-farm.txt', import.meta.url));

const ENTITIES = {
  amp: '&',
  lt: '<',
  gt: '>',
  quot: '"',
  apos: "'",
  nbsp: ' ',
  mdash: '—',
  ndash: '–',
  hellip: '…',
  lsquo: '‘',
  rsquo: '’',
  ldquo: '“',
  rdquo: '”',
};
const decode = (s) => s
  .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
  .replace(/&#x([\da-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
  .replace(/&(\w+);/g, (m, n) => ENTITIES[n.toLowerCase()] ?? m);

const res = await fetch(SOURCE);
if (!res.ok) throw new Error(`下載失敗：HTTP ${res.status}`);
const html = await res.text();

// 每個 <p>/<h*> 轉成一個以空行分隔的段落；<br> 保留成換行並縮排（歌詞、七誡）
let text = html
  .replace(/^[\s\S]*?<body[^>]*>/i, '')
  .replace(/<(script|style)[\s\S]*?<\/\1>/gi, '')
  .replace(/<br\s*\/?>\s*/gi, '\n    ')
  .replace(/<\/?(p|h\d|div|blockquote)[^>]*>/gi, '\n\n')
  .replace(/<[^>]+>/g, '');
text = decode(text)
  .split(/\n\s*\n/)
  .map((b) => b.replace(/[ \t]+$/gm, '').replace(/^\n+/, ''))
  .filter((b) => b.trim())
  .map((b) => (b.includes('\n    ') ? `    ${b.trim()}` : b.replace(/\s+/g, ' ').trim()))
  .join('\n\n');

// 去掉第一章之前的版權說明、與書末的 Gutenberg 頁尾
const start = text.search(/^Chapter I\b/m);
const end = text.search(/^THE END\b/m);
if (start < 0) throw new Error('找不到「Chapter I」，來源格式可能改了');
text = text.slice(start, end > start ? end : undefined).trim();
// Gutenberg AU 的章節標題是單獨一行的 "Chapter I"、"Chapter II"…，閱讀器會自動變成目錄

await writeFile(OUT, `${text}\n`, 'utf8');
console.log(`已寫入 ${OUT}（${text.length.toLocaleString()} 字元，${(text.match(/^Chapter /gm) || []).length} 章）`);
