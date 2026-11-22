// 聖經學英文：點單字查意思、跟讀評分
(() => {
  const { $, esc, toast } = App;

  /* ---------- 點單字 ---------- */
  let ctl = null, onWord = null;
  async function lookup(word, sentence, el) {
    if (onWord) onWord.classList.remove('on');
    onWord = el; if (el) el.classList.add('on');
    $('#check').hidden = true;
    $('#wordText').textContent = word;
    const out = $('#wordOut'); out.className = 'out wait'; out.textContent = '查詢中…';
    $('#word').hidden = false;
    App.speak(word, null, 0.8);
    if (ctl) ctl.abort();
    ctl = new AbortController(); const my = ctl;
    try {
      const url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-TW&hl=zh-TW&dt=t&dt=bd&q=' + encodeURIComponent(word);
      const data = await (await fetch(url, { signal: my.signal })).json();
      if (my !== ctl) return;
      const lines = [(data[0] || []).map((s) => (Array.isArray(s) ? s[0] || '' : '')).join('').trim()];
      if (Array.isArray(data[1])) data[1].slice(0, 4).forEach((e) => { if (Array.isArray(e) && Array.isArray(e[1])) lines.push((e[0] ? e[0] + '：' : '') + e[1].slice(0, 5).join('、')); });
      out.className = 'out'; out.textContent = lines.filter(Boolean).join('\n') || '查不到這個字。';
    } catch (e) {
      if (my !== ctl || (e && e.name === 'AbortError')) return;
      out.className = 'out wait'; out.textContent = '現在查不到（可能是網路不穩），請稍後再點一次。';
    }
  }
  App.lookup = lookup;
  $('#wordSay').onclick = () => App.speak($('#wordText').textContent, null, 0.7);
  $('#wordClose').onclick = () => { $('#word').hidden = true; if (onWord) onWord.classList.remove('on'); };

  /* ---------- 跟讀評分：用手機的語音辨識聽你唸，比對每個字 ---------- */
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const words = (t) => t.toLowerCase().replace(/[’‘]/g, "'").replace(/[^a-z0-9' ]+/g, ' ').split(/\s+/).filter(Boolean);
  // 最長共同子序列：找出目標句子裡哪些字有唸到
  function matchWords(target, heard) {
    const n = target.length, m = heard.length;
    const dp = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) dp[i][j] = target[i] === heard[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    const ok = new Array(n).fill(false);
    for (let i = 0, j = 0; i < n && j < m;) {
      if (target[i] === heard[j]) { ok[i] = true; i++; j++; } else if (dp[i + 1][j] >= dp[i][j + 1]) i++; else j++;
    }
    return ok;
  }
  let rec = null;
  function check(row) {
    if (!SR) { toast('這個瀏覽器不支援語音辨識，請用手機的 Chrome。'); return; }
    if (App.stop) App.stop();
    $('#word').hidden = true;
    const text = App.en(row);
    const tokens = text.match(/[A-Za-z0-9][A-Za-z0-9’']*|[^A-Za-z0-9]+/g) || [];
    $('#checkTitle').textContent = '🎤 請大聲唸出這一節…';
    $('#checkTarget').textContent = text;
    $('#checkHeard').textContent = '';
    $('#check').hidden = false;
    if (rec) try { rec.abort(); } catch {}
    rec = new SR();
    rec.lang = 'en-US'; rec.interimResults = false; rec.maxAlternatives = 3; rec.continuous = false;
    rec.onresult = (e) => {
      const alts = [...e.results[0]].map((a) => a.transcript);
      const target = words(text);
      let best = null;
      for (const h of alts) { const ok = matchWords(target, words(h)); const sc = ok.filter(Boolean).length; if (!best || sc > best.sc) best = { ok, sc, h }; }
      let k = 0;
      $('#checkTarget').innerHTML = tokens.map((t) => (/^[A-Za-z0-9]/.test(t) ? `<span class="${best.ok[k++] ? 'ok' : 'miss'}">${esc(t)}</span>` : esc(t))).join('');
      const pct = target.length ? Math.round((best.sc / target.length) * 100) : 0;
      $('#checkTitle').textContent = `${pct >= 90 ? '👏 很棒！' : pct >= 70 ? '👍 不錯！' : '💪 再試一次'}　唸對 ${pct}%（綠色是有聽到的字，紅色是沒聽清楚的字）`;
      $('#checkHeard').textContent = '手機聽到的是：' + best.h;
    };
    rec.onerror = (e) => {
      $('#checkTitle').textContent = e.error === 'not-allowed' ? '沒辦法使用麥克風，請在瀏覽器的網站設定裡允許麥克風。'
        : e.error === 'no-speech' ? '沒有聽到聲音，請按「🎤 跟讀」再試一次。' : '語音辨識失敗了，請再試一次。';
    };
    rec.onend = () => { if ($('#checkTitle').textContent.startsWith('🎤')) $('#checkTitle').textContent = '沒有聽清楚，請按「🎤 跟讀」再試一次。'; };
    try { rec.start(); } catch { toast('麥克風正在使用中，請稍後再試。'); }
  }
  App.check = check;
  $('#checkClose').onclick = () => { $('#check').hidden = true; if (rec) try { rec.abort(); } catch {} };
})();
