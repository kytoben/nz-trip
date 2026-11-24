import sys,json
APP='/tmp/claude-0/-home-user/d795addb-7998-5eb0-b370-a160b0710c12/scratchpad/app/'
s=open(APP+'index.html').read()
cfg=open('/tmp/claude-0/web/config.json').read().strip() if len(sys.argv)<2 else sys.argv[1]
def R(a,b):
    global s
    assert s.count(a)==1,a[:70]; s=s.replace(a,b)
R('景点按天上色，白色方块是住宿、取车和机场。点任意一个点即可导航。','景点按天上色，黑色方块是住宿、取车和机场。右上角可切换街道图和卫星图。')
R('renderNav(); render(); connect();','window.__boot = () => { renderNav(); render(); connect(); };')
R('db = await (window.claude?.use ? window.claude.use("db") : null);','db = window.__fbdb || null;')
R('登录同一个 Claude 账号，在电脑和手机上打开这个页面，看到的是同一份数据。','电脑和手机用同一个邮箱和口令解锁，看到的是同一份数据。</div><div class="row" style="margin-top:8px"><button type="button" class="btn sm ghost" id="logout-btn">在这台设备上退出</button>')
R('''    const dl = await (window.claude?.use ? window.claude.use("downloads") : null);
    if(!dl){ layer.querySelector("#bk-hint").textContent = "这里不能下载文件，请用“复制备份文本”。"; return; }
    try { await dl.save({filename:`旅行备份-${isoDate(new Date())}.json`, data:dump()}); } catch(e){ layer.querySelector("#bk-hint").textContent = "没有保存。"; }''','''    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([dump()], {type:"application/json"})); a.download = `旅行备份-${isoDate(new Date())}.json`; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);''')
R('''  layer.querySelector("#copy-btn").onclick''','''  const lo = layer.querySelector("#logout-btn"); if(lo) lo.onclick = () => window.__logout && window.__logout();
  layer.querySelector("#copy-btn").onclick''')
# geocode via OSM instead of claude sample
R('''    const sample = await (window.claude?.use ? window.claude.use("sample") : null);
    if(!sample){''','''    hint.textContent = "正在查找…"; hint.className = "hint";
    try { const r = await fetch("https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=nz&accept-language=zh,en&q=" + encodeURIComponent(v)).then(r => r.json());
      if(r && r[0]){ coordI.value = `${Number(r[0].lat).toFixed(4)}, ${Number(r[0].lon).toFixed(4)}`; hint.textContent = `找到：${String(r[0].display_name || "").split(",").slice(0,2).join(",")}（大致位置，可在地图上核对）`; return; }
    } catch(e){}
    const sample = null;
    if(!sample){''')
lock='''<div id="lock" hidden><div class="lock-card"><div class="lock-ic"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></div><h1 class="lock-t">旅行手帐</h1><p class="lock-s">这是私人页面，请输入邮箱和口令解锁。<br>每台设备只需解锁一次。</p><form id="lock-form" autocomplete="on"><input id="lock-email" type="email" autocomplete="username" placeholder="邮箱" required><input id="lock-pw" type="password" autocomplete="current-password" placeholder="口令" required><button class="btn" type="submit" id="lock-go">解锁</button><div class="lock-err" id="lock-err"></div></form></div></div>
<style>
#app-root[hidden]{display:none!important}
#lock{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;padding:24px;background:linear-gradient(180deg,#03050b 0%,#07122a 45%,#0d2a3f 80%,#12384a 100%);color:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Helvetica,Arial,sans-serif}
#lock[hidden]{display:none}
.lock-card{width:min(360px,100%);text-align:center}
.lock-ic{width:56px;height:56px;border-radius:18px;margin:0 auto 18px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.1);color:#9fd8ff}
.lock-t{font-size:34px;letter-spacing:-.03em;margin:0;font-weight:700;background:linear-gradient(95deg,#fff 20%,#bfe9ff 60%,#c6ffe4);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.lock-s{color:rgba(245,245,247,.68);font-size:15px;line-height:1.6;margin:10px 0 26px}
#lock-form{display:flex;flex-direction:column;gap:10px}
#lock-form input{height:48px;border-radius:14px;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.08);color:#fff;padding:0 16px;font-size:16px;outline:none}
#lock-form input:focus{border-color:#5ac8fa;background:rgba(255,255,255,.12)}
#lock-form input::placeholder{color:rgba(245,245,247,.45)}
#lock-go{height:48px;border-radius:14px;border:0;background:#0071e3;color:#fff;font-size:16px;font-weight:600;margin-top:4px;cursor:pointer}
#lock-go:disabled{opacity:.6}
.lock-err{min-height:20px;color:#ff8a80;font-size:14px}
</style>
<script type="module">
import {initializeApp, getAuth, onAuthStateChanged, signInWithEmailAndPassword, setPersistence, browserLocalPersistence, signOut, initializeFirestore, persistentLocalCache, persistentMultipleTabManager, doc, collection, onSnapshot, setDoc, deleteDoc} from "./fb.js";
const CFG = __CFG__;
const app = initializeApp(CFG), auth = getAuth(app);
let fs; try { fs = initializeFirestore(app, {localCache: persistentLocalCache({tabManager: persistentMultipleTabManager()})}); } catch(e){ fs = initializeFirestore(app, {}); }
const wrapDoc = s => ({exists: s.exists(), data: () => s.data(), metadata: {fromCache: s.metadata.fromCache}});
function mk(uid){
  const base = ["users", uid];
  return {
    doc(path){ const r = doc(fs, ...base, ...path.split("/")); return {onSnapshot: (cb, err) => onSnapshot(r, {includeMetadataChanges:true}, s => cb(wrapDoc(s)), err), set: d => setDoc(r, d)}; },
    collection(c){ const cr = collection(fs, ...base, c); return {
      onSnapshot: (cb, err) => onSnapshot(cr, {includeMetadataChanges:true}, s => cb({docs: s.docs.map(d => ({id: d.id, data: () => d.data()})), metadata: {fromCache: s.metadata.fromCache}}), err),
      doc: id => { const r = doc(cr, id); return {set: d => setDoc(r, d), delete: () => deleteDoc(r)}; }}; }
  };
}
const lock = document.getElementById("lock"), root = document.getElementById("app-root");
let booted = false;
window.__logout = async () => { try { localStorage.removeItem("nztrip-cache-v1"); } catch(e){} await signOut(auth); location.reload(); };
onAuthStateChanged(auth, user => {
  if(user){ lock.hidden = true; root.hidden = false; if(!booted){ booted = true; window.__fbdb = mk(user.uid); window.__boot(); } }
  else { try { localStorage.removeItem("nztrip-cache-v1"); } catch(e){} root.hidden = true; lock.hidden = false; }
});
document.getElementById("lock-form").addEventListener("submit", async e => {
  e.preventDefault(); const btn = document.getElementById("lock-go"), err = document.getElementById("lock-err");
  btn.disabled = true; err.textContent = "";
  try { await setPersistence(auth, browserLocalPersistence); await signInWithEmailAndPassword(auth, document.getElementById("lock-email").value.trim(), document.getElementById("lock-pw").value); }
  catch(x){ err.textContent = /network/.test(x.code || "") ? "网络连不上，请稍后再试" : /too-many/.test(x.code || "") ? "尝试太多次，请过几分钟再试" : "邮箱或口令不对"; }
  btn.disabled = false;
});
</script>'''.replace('__CFG__',cfg)
head='<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="旅行手帐"><link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon.svg">'
# split head part (title/meta/style) from body
i=s.index('</style>')+len('</style>')
headpart, body = s[:i], s[i:]
rm_js=open('/tmp/claude-0/web/realmap.js').read(); rm_css=open('/tmp/claude-0/web/realmap.css').read()
head+='<link rel="stylesheet" href="leaflet.css"><script src="leaflet.js"></script>'
body=body.replace('window.__boot = () => {', rm_js+'\nwindow.__boot = () => {',1)+'<style>'+rm_css+'</style>'
out=head+headpart+'</head><body style="margin:0">'+'<div id="app-root" hidden>'+body+'</div>'+lock+'</body></html>'
open('/tmp/claude-0/web/site/index.html','w').write(out)
print(len(out))
