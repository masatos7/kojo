import streamlit as st
import streamlit.components.v1 as components

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }

[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
[data-testid="stHeader"], .stAppHeader {
    background: transparent !important; height: 0 !important;
    pointer-events: none !important; z-index: 0 !important;
}
[data-testid="stAppViewContainer"] { background: #f8fafc !important; }
.stMainBlockContainer {
    padding: 60px 0 0 0 !important;
    max-width: 100% !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stVerticalBlockWithBorder"] { padding: 0 !important; }

/* ── ヒーロー ── */
.hero {
    background: #ffffff;
    padding: 6rem 2rem 5.5rem;
    text-align: center;
    border-bottom: 1px solid #e5e7eb;
}
.hero h1 {
    font-family: 'Inter', sans-serif;
    font-size: 4.8rem; font-weight: 900; color: #0f172a;
    letter-spacing: -.02em; margin: 0 0 1.2rem;
    line-height: 1.05;
}
.hero h1 span { color: #2563eb; }
.hero p {
    font-size: 1.05rem; color: #64748b;
    margin-bottom: 2.8rem; line-height: 1.9;
}
.hero b { color: #0f172a; }
[data-nav] { text-decoration: none !important; }

.hero-btn {
    display: inline-block; background: #2563eb; color: #fff !important;
    text-decoration: none !important; padding: .95rem 2.4rem; border-radius: 8px;
    font-size: .95rem; font-weight: 700; letter-spacing: .01em;
    box-shadow: 0 4px 14px rgba(37,99,235,.35);
    transition: background .2s, transform .1s, box-shadow .2s;
    cursor: pointer;
}
.hero-btn:hover {
    background: #1d4ed8; transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(37,99,235,.45);
}

/* ── ギャラリー ── */
.gallery-section {
    background: #f8fafc;
    padding: 4rem 2.5rem 5rem;
}
.gallery-section h2 {
    font-size: 1.5rem; font-weight: 800; color: #0f172a;
    letter-spacing: -.01em; margin: 0 0 1.5rem;
}

/* ── フィルター ── */
.filter-box {
    display: flex; flex-direction: column; align-items: center;
    margin-bottom: 2rem;
    border: 1px solid #e5e7eb; border-radius: 12px;
    padding: 1rem 1.5rem; background: #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.filter-label {
    font-size: .72rem; font-weight: 700; color: #94a3b8;
    letter-spacing: .1em; text-transform: uppercase; margin-bottom: .6rem;
}
.filter-bar { display: flex; gap: .75rem; flex-wrap: wrap; justify-content: center; }
.filter-bar select {
    padding: .45rem .9rem; border-radius: 8px;
    border: 1px solid #e5e7eb; background: #fff;
    font-size: .85rem; color: #374151; cursor: pointer;
    font-family: 'Inter', sans-serif;
}
.filter-bar select:focus { outline: 2px solid #2563eb; outline-offset: 1px; }

/* ── カード ── */
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: 1.2rem; }
.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
    text-decoration: none; color: inherit; display: block;
    transition: border-color .2s, transform .15s, box-shadow .2s;
    cursor: pointer;
}
.card:hover {
    border-color: #2563eb;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(37,99,235,.1);
}

.card-thumb { position: relative; }
.card-thumb img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; }
.card-thumb-overlay {
    position: absolute; bottom: 0; left: 0; right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,.65));
    padding: .5rem .8rem .6rem;
    display: flex; justify-content: space-between; align-items: flex-end;
}
.overlay-sport { color: #fff; font-size: .85rem; font-weight: 700; }
.overlay-age   { color: #cbd5e1; font-size: .78rem; }

.card-body { padding: .9rem 1.2rem; }
.card-meta  { color: #94a3b8; font-size: .8rem; display: block; }
.card-link  { color: #2563eb; font-size: .85rem; font-weight: 600; display: block; margin-top: .4rem; }
.gallery-empty { text-align: center; color: #94a3b8; padding: 3rem 0; font-size: .95rem; }

/* ── インナーページ共通 ── */
.inner-wrap { max-width: 760px; margin: 0 auto; padding: 2.5rem 1.5rem 4rem; }
.inner-wrap h1 { color: #0f172a; font-size: 1.8rem; font-weight: 800; margin-bottom: .4rem; }
.subtitle { color: #64748b !important; }
hr.inner-divider { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
</style>
"""


def inject_styles():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header():
    components.html("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:60px;overflow:hidden;background:#ffffff}
header{
  height:60px;width:100%;display:flex;align-items:center;padding:0 2.5rem;
  background:#ffffff;border-bottom:1px solid #f1f5f9;
  font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  position:relative;
}
.logo{
  font-size:1.3rem;font-weight:800;color:#0f172a;
  cursor:pointer;letter-spacing:.06em;user-select:none;flex-shrink:0;
}
.logo span{color:#2563eb}
.logo:hover{color:#2563eb}
nav{position:absolute;left:50%;transform:translateX(-50%);white-space:nowrap}
nav a{
  margin:0 1rem;font-size:.88rem;font-weight:600;
  color:#64748b;cursor:pointer;user-select:none;
  text-decoration:none;transition:color .15s;
}
nav a:hover{color:#0f172a}
.upload-btn{
  margin-left:auto;
  background:#2563eb;color:#fff !important;
  font-size:.82rem;font-weight:700;
  padding:.45rem 1.1rem;border-radius:7px;
  cursor:pointer;border:none;
  font-family:'Inter',sans-serif;
  text-decoration:none;
  transition:background .15s;
  flex-shrink:0;
}
.upload-btn:hover{background:#1d4ed8}
</style>
</head>
<body>
<header>
  <span class="logo" onclick="go('/')">KO<span>J</span>O</span>
  <nav>
    <a onclick="go('/')">ホーム</a>
    <a onclick="go('/guides')">練習ガイド</a>
  </nav>
  <span class="upload-btn" onclick="go('/upload')">動画を投稿</span>
</header>
<script>
function go(u){
  try{
    var a=window.parent.document.createElement('a');
    a.href=u; a.style.display='none';
    window.parent.document.body.appendChild(a);
    a.click();
    window.parent.document.body.removeChild(a);
  }catch(e){}
}
(function(){
  try{
    var pdoc=window.parent.document;
    pdoc.addEventListener('click',function(e){
      var el=e.target;
      while(el&&!el.dataset.nav) el=el.parentElement;
      if(!el||!el.dataset.nav) return;
      e.preventDefault(); e.stopPropagation();
      var a=pdoc.createElement('a');
      a.href=el.dataset.nav; a.style.display='none';
      pdoc.body.appendChild(a); a.click(); pdoc.body.removeChild(a);
    });
    pdoc.addEventListener('change',function(e){
      var el=e.target;
      if(!el.dataset||!el.dataset.filter) return;
      var url=new URL(window.parent.location.href);
      if(el.value){ url.searchParams.set(el.dataset.filter,el.value); }
      else { url.searchParams.delete(el.dataset.filter); }
      var a=pdoc.createElement('a');
      a.href=url.toString(); a.style.display='none';
      pdoc.body.appendChild(a); a.click(); pdoc.body.removeChild(a);
    });
  }catch(e){}
})();
(function(){
  try{
    var ifr=window.frameElement;
    var box=ifr.parentElement;
    box.style.cssText=
      'position:fixed!important;top:0!important;left:0!important;'+
      'right:0!important;z-index:9999!important;height:60px!important;'+
      'padding:0!important;margin:0!important;';
    ifr.style.cssText=
      'width:100%!important;height:60px!important;'+
      'border:none!important;display:block!important;';
  }catch(e){}
})();
</script>
</body>
</html>""", height=60, scrolling=False)
