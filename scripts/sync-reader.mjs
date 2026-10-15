// 把 public/reader/index.html 同步到 GitHub Pages（docs/），並蓋上版本號。
// 每次改完閱讀器執行：node scripts/sync-reader.mjs
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const src = `${root}public/reader/index.html`;
const html = readFileSync(src, 'utf8');
const body = html.replace(/const APP_VERSION = '[^']*';/, "const APP_VERSION = '';");
const v = createHash('sha1').update(body).digest('hex').slice(0, 10);
const stamped = body.replace("const APP_VERSION = '';", `const APP_VERSION = '${v}';`);
writeFileSync(src, stamped);
const lines = stamped.split('\n');
lines.splice(1, 0, '<!-- 這是 public/reader/index.html 的複本，給 GitHub Pages 用：請改 public/reader/index.html 後執行 node scripts/sync-reader.mjs -->');
writeFileSync(`${root}docs/index.html`, lines.join('\n'));
const json = `${JSON.stringify({ v })}\n`;
writeFileSync(`${root}docs/version.json`, json);
writeFileSync(`${root}public/reader/version.json`, json);
console.log(`reader version ${v}`);
