import axios from 'axios';

// Google 翻譯網頁版用的免費介面（非官方，量大時可能被限流）
const client = axios.create({
  baseURL: 'https://translate.googleapis.com',
  timeout: 8000,
});

// 把 Google 回傳的陣列整理成閱讀器要顯示的文字：
// 第一行是翻譯；單字的話，接著列出各詞性的常見意思
const formatTranslation = (data) => {
  if (!Array.isArray(data) || !Array.isArray(data[0])) return '';
  const text = data[0].map((seg) => (Array.isArray(seg) ? seg[0] || '' : '')).join('').trim();
  const lines = [text];
  if (Array.isArray(data[1])) {
    data[1].slice(0, 4).forEach((entry) => {
      if (!Array.isArray(entry) || !Array.isArray(entry[1])) return;
      const pos = entry[0] ? `${entry[0]}：` : '';
      lines.push(`${pos}${entry[1].slice(0, 5).join('、')}`);
    });
  }
  return lines.filter(Boolean).join('\n');
};

const translate = async ({ q, sl = 'auto', tl = 'zh-TW' }) => {
  const { data } = await client.get('/translate_a/single', {
    params: {
      client: 'gtx', sl, tl, hl: tl, dt: ['t', 'bd'], dj: 0, q,
    },
    paramsSerializer: { indexes: null },
  });
  return formatTranslation(data);
};

export {
  formatTranslation,
  translate,
};
