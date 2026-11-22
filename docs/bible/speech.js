// 聖經學英文：英文朗讀、整章播放、跟讀模式
(() => {
  const { $, prefs, toast } = App;
  const synth = window.speechSynthesis;
  let voices = [];

  function loadVoices() {
    if (!synth) return;
    voices = synth.getVoices().filter((v) => /^en[-_]/i.test(v.lang));
    voices.sort((a, b) => (/en[-_]US/i.test(b.lang) - /en[-_]US/i.test(a.lang)) || (/google|natural|samantha/i.test(b.name) - /google|natural|samantha/i.test(a.name)));
    $('#voice').innerHTML = voices.length
      ? voices.map((v) => `<option value="${App.esc(v.name)}">${App.esc(v.name)}（${App.esc(v.lang)}）</option>`).join('')
      : '<option value="">使用系統預設的英文聲音</option>';
    if (prefs.voice && voices.some((v) => v.name === prefs.voice)) $('#voice').value = prefs.voice;
  }
  if (synth) { loadVoices(); synth.onvoiceschanged = loadVoices; }
  $('#voice').onchange = () => { prefs.voice = $('#voice').value; App.save(); App.speak('Hello, nice to meet you.'); };
  const pickVoice = () => voices.find((v) => v.name === prefs.voice) || voices[0] || null;

  // 念一段英文；念完時呼叫 done(花了幾毫秒)
  function speak(text, done, rate) {
    if (!synth) { toast('這個瀏覽器不支援朗讀，請用 Chrome 或 Safari。'); return; }
    synth.cancel();
    const u = new SpeechSynthesisUtterance(text);
    const v = pickVoice(); if (v) { u.voice = v; u.lang = v.lang; } else u.lang = 'en-US';
    u.rate = rate || prefs.rate;
    const t0 = Date.now();
    u.onend = () => done && done(Date.now() - t0);
    u.onerror = () => done && done(-1);
    synth.speak(u);
  }
  App.speak = speak;

  // 整章播放：一節一節念，畫面跟著捲；跟讀模式會在每節之後停一下讓你跟著唸
  let playing = false, idx = 0, timer = 0, shadow = false;
  const mark = (i) => {
    document.querySelectorAll('.verse.now').forEach((el) => el.classList.remove('now'));
    const el = document.querySelector(`.verse[data-i="${i}"]`);
    if (el) { el.classList.add('now'); el.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
  };
  function next() {
    if (!playing) return;
    if (idx >= App.rows.length) { stop(); toast('這一章念完了'); return; }
    const i = idx; mark(i);
    speak(App.en(App.rows[i]), (ms) => {
      if (!playing) return;
      if (ms < 0) { stop(); toast('朗讀失敗了，請到「設定」換一個英文聲音再試。'); return; }
      idx = i + 1;
      const wait = shadow ? Math.max(1500, ms * prefs.gap) : 350;
      timer = setTimeout(next, wait);
    });
  }
  function start(from) {
    playing = true; idx = from || 0;
    $('#play').textContent = '⏸ 停止';
    next();
  }
  function stop() {
    playing = false; clearTimeout(timer);
    if (synth) synth.cancel();
    $('#play').textContent = '▶ 播放本章';
  }
  App.stop = stop;
  // 從畫面上看到的第一節開始播
  const firstVisible = () => {
    const els = [...document.querySelectorAll('.verse')];
    const k = els.findIndex((el) => el.getBoundingClientRect().bottom > 70);
    return k < 0 ? 0 : k;
  };
  $('#play').onclick = () => (playing ? stop() : start(firstVisible()));
  $('#shadow').onclick = () => {
    shadow = !shadow;
    $('#shadow').setAttribute('aria-pressed', shadow);
    toast(shadow ? '跟讀模式：每念完一節會停一下，請跟著大聲唸一遍' : '跟讀模式已關閉');
  };
  App.sayVerse = (i) => { stop(); mark(i); speak(App.en(App.rows[i])); };
})();
