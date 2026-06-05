import express from 'express';
import { handleEvents, printPrompts } from '../app/index.js';
import config from '../config/index.js';
import { validateLineSignature } from '../middleware/index.js';
import { reply } from '../services/line.js';
import storage from '../storage/index.js';
import { fetchVersion, getVersion } from '../utils/index.js';

const app = express();

app.use(express.json({
  verify: (req, res, buf) => {
    req.rawBody = buf.toString();
  },
}));

app.get('/', (req, res) => {
  if (config.APP_URL) {
    res.redirect(config.APP_URL);
    return;
  }
  res.sendStatus(200);
});

app.get('/info', async (req, res) => {
  const currentVersion = getVersion();
  const latestVersion = await fetchVersion();
  res.status(200).send({ currentVersion, latestVersion });
});

app.post(config.APP_WEBHOOK_PATH, validateLineSignature, async (req, res) => {
  const events = req.body.events || [];
  console.log('[webhook] received', events.length, 'event(s):', JSON.stringify(events.map((e) => ({ type: e.type, sourceType: e.source?.type }))));
  try {
    await storage.initialize();
    for (const event of events) {
      if (event.type === 'join' && event.replyToken) {
        console.log('[webhook] bot joined group:', event.source?.groupId);
        await reply({
          replyToken: event.replyToken,
          messages: [{ type: 'text', text: `大家好！我是${config.BOT_NAME}，叫我名字就可以問我問題囉！` }],
        });
      }
    }
    await handleEvents(events);
    res.sendStatus(200);
  } catch (err) {
    console.error('[webhook] error:', err.message);
    res.sendStatus(500);
  }
  if (config.APP_DEBUG) printPrompts();
});

if (config.APP_PORT) {
  app.listen(config.APP_PORT);
}

export default app;
