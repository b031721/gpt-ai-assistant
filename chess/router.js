import express from 'express';
import fs from 'fs';
import config from '../config/index.js';

const PAGE_URL = new URL('../docs/chess/index.html', import.meta.url);
let page = null;

const router = express.Router();

router.get(['/chess', '/chess/', '/chess/index.html'], (req, res) => {
  if (!page || config.APP_DEBUG) page = fs.readFileSync(PAGE_URL, 'utf8');
  res.type('html').send(page);
});

export default router;
