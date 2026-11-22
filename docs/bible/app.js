// 聖經學英文：主程式（讀章、顯示、設定、句子本）
(() => {
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };
  const prefs = Object.assign({ v: 1, show: 'both', rate: 0.8, gap: 1.5, voice: '', size: 19, book: 42, ch: 15 }, store.get('bible:prefs', {}));
  const App = window.App = { $, esc, store, prefs, rows: [], toast };

  function toast(msg) {
    const t = $('#toast'); t.textContent = msg; t.hidden = false;
    clearTimeout(toast.t); toast.t = setTimeout(() => { t.hidden = true; }, 2800);
  }
  App.save = () => store.set('bible:prefs', prefs);
  App.ref = (b, c, v) => `${BOOKS[b - 1][0]} ${c}:${v}`;
  App.en = (row) => row[prefs.v] || row[1] || row[2];

  // 英文每個字包成一個可以點的小方塊
  const wrapWords = (t) => esc(t).replace(/[A-Za-z][A-Za-z’']*/g, (w) => `<span class="w">${w}</span>`);

  function applyPrefs() {
    document.body.classList.toggle('show-en', prefs.show === 'en');
    document.body.classList.toggle('show-quiz', prefs.show === 'quiz');
    document.documentElement.style.setProperty('--size', prefs.size + 'px');
    const on = (sel, attr, val) => document.querySelectorAll(sel + ' button').forEach((b) => b.classList.toggle('on', b.dataset[attr] === String(val)));
    on('#verSeg', 'v', prefs.v); on('#showSeg', 's', prefs.show); on('#rateSeg', 'r', prefs.rate); on('#gapSeg', 'g', prefs.gap); on('#sizeSeg', 'z', prefs.size);
    App.save();
  }
  App.applyPrefs = applyPrefs;

  function savedList() { return store.get('bible:saved', []); }
  const savedKey = (b, c, v) => `${b}-${c}-${v}`;

  function render() {
    const b = prefs.book, c = prefs.ch, saved = new Set(savedList().map((s) => s.k));
    $('#where').textContent = `${BOOKS[b - 1][0]} ${c}　${BOOKS[b - 1][1]} ${c}`;
    $('#list').innerHTML = App.rows.map((r, i) => `<article class="verse" data-i="${i}" id="v${r[0]}">
        <p class="en"><sup>${r[0]}</sup>${wrapWords(App.en(r))}</p>
        <p class="zh">${esc(r[3])}</p>
        <div class="acts"><button data-act="say">🔊 聽</button><button data-act="check">🎤 跟讀</button><button data-act="save" class="${saved.has(savedKey(b, c, r[0])) ? 'on' : ''}">${saved.has(savedKey(b, c, r[0])) ? '★ 已收藏' : '☆ 收藏'}</button></div>
      </article>`).join('') + `<div class="chapter-end">${esc(BOOKS[b - 1][0])} 第 ${c} 章完<br>${c < BOOKS[b - 1][2] || b < 66 ? '<button id="goNext">下一章 ›</button>' : ''}</div>`;
    const n = $('#goNext'); if (n) n.onclick = () => step(1);
    document.title = `${BOOKS[b - 1][0]} ${c} | 聖經學英文`;
  }
  App.render = render;

  async function open(b, c, verse) {
    if (App.stop) App.stop();
    prefs.book = b; prefs.ch = c; App.save();
    $('#list').innerHTML = '<p class="chapter-end">載入中…</p>';
    try {
      const r = await fetch(`data/${b}-${c}.json`);
      if (!r.ok) throw new Error(r.status);
      App.rows = await r.json();
    } catch {
      $('#list').innerHTML = '<p class="chapter-end">載入失敗，請確認網路後再試一次。</p>'; return;
    }
    render();
    const el = verse && document.getElementById('v' + verse);
    if (el) { el.scrollIntoView({ block: 'center' }); el.classList.add('now'); setTimeout(() => el.classList.remove('now'), 2000); } else scrollTo(0, 0);
  }
  App.open = open;
  function step(d) {
    let b = prefs.book, c = prefs.ch + d;
    if (c < 1) { if (b === 1) return; b -= 1; c = BOOKS[b - 1][2]; }
    if (c > BOOKS[b - 1][2]) { if (b === 66) return; b += 1; c = 1; }
    open(b, c);
  }
  $('#prevCh').onclick = () => step(-1);
  $('#nextCh').onclick = () => step(1);

  // 經節上的按鈕、點單字
  $('#list').addEventListener('click', (e) => {
    const art = e.target.closest('.verse'); if (!art) return;
    const row = App.rows[+art.dataset.i];
    const act = e.target.closest('[data-act]');
    if (act) {
      if (act.dataset.act === 'say') App.sayVerse(+art.dataset.i);
      if (act.dataset.act === 'check') App.check(row);
      if (act.dataset.act === 'save') toggleSave(row, act);
      return;
    }
    const en = e.target.closest('.en');
    if (en && prefs.show === 'quiz' && !en.classList.contains('reveal')) { en.classList.add('reveal'); return; }
    const w = e.target.closest('.w');
    if (w) App.lookup(w.textContent, App.en(row), w);
  });

  function toggleSave(row, btn) {
    const k = savedKey(prefs.book, prefs.ch, row[0]);
    let list = savedList();
    if (list.some((s) => s.k === k)) { list = list.filter((s) => s.k !== k); btn.classList.remove('on'); btn.textContent = '☆ 收藏'; }
    else { list.unshift({ k, b: prefs.book, c: prefs.ch, v: row[0], en: App.en(row), zh: row[3] }); btn.classList.add('on'); btn.textContent = '★ 已收藏'; toast('已收進「我的句子本」（右上角 ☆）'); }
    store.set('bible:saved', list);
  }

  // 抽屜：選章、設定、句子本
  const sheets = ['#picker', '#settings', '#saved'];
  const close = () => sheets.forEach((s) => { $(s).hidden = true; });
  document.querySelectorAll('[data-close]').forEach((b) => { b.onclick = close; });
  App.closeSheets = close;

  $('#where').onclick = () => { close(); $('#picker').hidden = false; $('#chapters').hidden = true; };
  $('#picks').innerHTML = PICKS.map(([b, c, d]) => `<button data-b="${b}" data-c="${c}"><b>${esc(BOOKS[b - 1][0])} ${c}章（${esc(BOOKS[b - 1][1])} ${c}）</b><span>${esc(d)}</span></button>`).join('');
  $('#picks').onclick = (e) => { const p = e.target.closest('button'); if (p) { close(); open(+p.dataset.b, +p.dataset.c); } };
  const bookBtn = (i) => `<button data-b="${i + 1}">${esc(BOOKS[i][0])}</button>`;
  $('#ot').innerHTML = BOOKS.slice(0, 39).map((_, i) => bookBtn(i)).join('');
  $('#nt').innerHTML = BOOKS.slice(39).map((_, i) => bookBtn(i + 39)).join('');
  const chooseBook = (e) => {
    const btn = e.target.closest('button'); if (!btn) return;
    const b = +btn.dataset.b, n = BOOKS[b - 1][2];
    if (n === 1) { close(); open(b, 1); return; }
    document.querySelectorAll('.books button').forEach((x) => x.classList.toggle('on', x === btn));
    const box = $('#chapters');
    box.innerHTML = `<p>${esc(BOOKS[b - 1][0])}：選一章</p>` + Array.from({ length: n }, (_, i) => `<button data-c="${i + 1}">${i + 1}</button>`).join('');
    box.hidden = false;
    btn.parentElement.after(box);
    box.onclick = (ev) => { const cb = ev.target.closest('[data-c]'); if (cb) { close(); open(b, +cb.dataset.c); } };
    box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  };
  $('#ot').onclick = chooseBook; $('#nt').onclick = chooseBook;

  $('#btnSet').onclick = () => { close(); $('#settings').hidden = false; };
  $('#verSeg').onclick = (e) => { const b = e.target.closest('button'); if (b) { prefs.v = +b.dataset.v; applyPrefs(); render(); } };
  $('#showSeg').onclick = (e) => { const b = e.target.closest('button'); if (b) { prefs.show = b.dataset.s; applyPrefs(); render(); } };
  $('#rateSeg').onclick = (e) => { const b = e.target.closest('button'); if (b) { prefs.rate = +b.dataset.r; applyPrefs(); } };
  $('#gapSeg').onclick = (e) => { const b = e.target.closest('button'); if (b) { prefs.gap = +b.dataset.g; applyPrefs(); } };
  $('#sizeSeg').onclick = (e) => { const b = e.target.closest('button'); if (b) { prefs.size = +b.dataset.z; applyPrefs(); } };

  $('#btnSaved').onclick = () => { close(); showSaved(); $('#saved').hidden = false; };
  function showSaved() {
    const list = savedList();
    $('#savedList').innerHTML = list.length ? list.map((s, i) => `<li>
        <div class="ref">${esc(App.ref(s.b, s.c, s.v))}</div>
        <p class="en">${esc(s.en)}</p><p class="zh">${esc(s.zh)}</p>
        <div class="row"><button data-say="${i}">🔊 聽</button><button data-go="${i}">到這一節</button><button data-del="${i}">移除</button></div>
      </li>`).join('') : '<li class="empty">還沒有收藏的句子。看到想記下來的句子，按它下面的「☆ 收藏」，就會出現在這裡。</li>';
    $('#savedList').onclick = (e) => {
      const t = e.target.closest('button'); if (!t) return;
      const all = savedList();
      if (t.dataset.say) App.speak(all[+t.dataset.say].en);
      if (t.dataset.go) { const s = all[+t.dataset.go]; close(); open(s.b, s.c, s.v); }
      if (t.dataset.del) { all.splice(+t.dataset.del, 1); store.set('bible:saved', all); showSaved(); render(); }
    };
  }

  applyPrefs();
  addEventListener('load', () => open(prefs.book, prefs.ch));
})();
