import express from 'express';
import fs from 'fs';
import config from '../config/index.js';
import {
  createChatCompletion, ROLE_AI, ROLE_HUMAN, ROLE_SYSTEM,
} from '../services/openai.js';

const PAGE_URL = new URL('./index.html', import.meta.url);
let page = null;
const loadPage = () => {
  if (!page || config.APP_DEBUG) page = fs.readFileSync(PAGE_URL, 'utf8');
  return page;
};

const SYSTEM_PROMPT = [
  '你是一位親切、有耐心的中國象棋教練，正在指導一位學生和電腦對弈。',
  '學生執紅方（棋盤下方），電腦執黑方（棋盤上方）。',
  '請一律使用繁體中文回答，口吻像老師在旁邊陪下棋。',
  '關於具體棋步、局勢好壞與威脅，一律以提供的「引擎分析」為準，不要自己捏造棋步或棋子位置；引擎沒提到的變化要說明只是方向性的建議。',
  '重點是教學生「怎麼思考」：先看對方意圖、再檢查自身安全、再找機會、最後訂計畫。',
  '回答精簡清楚，盡量在 250 字以內，可以用條列。',
].join('\n');

const str = (v, max) => (typeof v === 'string' ? v.slice(0, max) : '');

const router = express.Router();

router.get(['/xiangqi', '/xiangqi/', '/xiangqi/index.html'], (req, res) => {
  res.type('html').send(loadPage());
});

router.get('/xiangqi/api/status', (req, res) => {
  res.json({ llm: Boolean(config.OPENAI_API_KEY) });
});

router.post('/xiangqi/api/ask', async (req, res) => {
  if (!config.OPENAI_API_KEY) {
    res.status(503).json({ error: 'OPENAI_API_KEY is not configured' });
    return;
  }
  const body = req.body || {};
  const question = str(body.question, 500).trim();
  if (!question) {
    res.status(400).json({ error: 'question is required' });
    return;
  }
  const chat = (Array.isArray(body.chat) ? body.chat : [])
    .slice(-6)
    .filter((m) => m && (m.role === ROLE_HUMAN || m.role === ROLE_AI))
    .map((m) => ({ role: m.role, content: str(m.content, 1000) }));
  const context = [
    `【目前棋盤】\n${str(body.board, 2000)}`,
    `【棋譜】${str(body.moves, 3000) || '（尚未開始）'}`,
    `【引擎分析】\n${str(body.engine, 2000) || '（無）'}`,
    `【學生的問題】${question}`,
  ].join('\n\n');
  try {
    const { data } = await createChatCompletion({
      messages: [
        { role: ROLE_SYSTEM, content: SYSTEM_PROMPT },
        ...chat,
        { role: ROLE_HUMAN, content: context },
      ],
      maxTokens: 700,
      temperature: 0.5,
    });
    const answer = data?.choices?.[0]?.message?.content?.trim();
    res.json({ answer: answer || '抱歉，我暫時想不到好的回答，換個方式問問看？' });
  } catch (err) {
    console.error('[xiangqi] ask error:', err.message);
    res.status(502).json({ error: err.message });
  }
});

export default router;
