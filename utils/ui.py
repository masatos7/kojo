import base64
import streamlit as st

_CSS = """
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
[data-testid="stHeader"], .stAppHeader {
    background: transparent !important; height: 0 !important;
    pointer-events: none !important; z-index: 0 !important;
}
[data-testid="stAppViewContainer"] { background: #ffffff !important; }
.stMainBlockContainer { padding: 60px 0 0 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stVerticalBlockWithBorder"] { padding: 0 !important; }

.hero {
    background: linear-gradient(140deg, #0f172a 0%, #1e3a5f 60%, #164e63 100%);
    padding: 7rem 2rem 6rem; text-align: center;
}
.hero h1 {
    font-size: 4.5rem; font-weight: 900; color: #ffffff;
    letter-spacing: .12em; margin: 0 0 1rem;
}
.hero p { font-size: 1.1rem; color: #ffffff; margin-bottom: 2.5rem; line-height: 1.9; }
.hero b { color: #e2e8f0; }
/* data-nav はブラウザデフォルトの下線を除去 */
[data-nav] { text-decoration: none !important; }

.hero-btn {
    display: inline-block; background: #ff0808; color: #fff !important;
    text-decoration: none !important; padding: .9rem 2.2rem; border-radius: 8px;
    font-size: 1rem; font-weight: 600;
    box-shadow: 0 6px 20px rgba(0,0,0,.35);
    transition: background .2s, transform .1s, box-shadow .2s;
    cursor: pointer;
}
.hero-btn:hover {
    background: #ff9b42; transform: translateY(1px);
    box-shadow: 0 2px 8px rgba(0,0,0,.45);
}

.gallery-section { background: #f1f5f9; padding: 3.5rem 2.5rem 5rem; }
.gallery-section h2 { font-size: 1.5rem; font-weight: 700; color: #0f172a; margin: 0 0 1.2rem; }

/* フィルターボックス */
.filter-box {
    display: flex; flex-direction: column; align-items: center;
    margin-bottom: 1.8rem;
    border: 1px solid #e5e7eb; border-radius: 12px;
    padding: 1rem 1.5rem; background: #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.filter-label {
    font-size: .78rem; font-weight: 700; color: #64748b;
    letter-spacing: .08em; text-transform: uppercase;
    margin-bottom: .6rem;
}
.filter-bar { display: flex; gap: .75rem; flex-wrap: wrap; justify-content: center; }
.filter-bar select {
    padding: .45rem .9rem; border-radius: 8px;
    border: 1px solid #e5e7eb; background: #fff;
    font-size: .85rem; color: #374151; cursor: pointer;
    box-shadow: 0 1px 2px rgba(0,0,0,.05);
}
.filter-bar select:focus { outline: 2px solid #2563eb; outline-offset: 1px; }

.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: 1.5rem; }
.card {
    background: #ffffff; border-radius: 12px; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,.08); text-decoration: none;
    color: inherit; display: block; transition: box-shadow .2s, transform .15s;
    cursor: pointer;
}
.card:hover { box-shadow: 0 6px 16px rgba(0,0,0,.12); transform: translateY(-3px); }

/* サムネールオーバーレイ */
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

.card-body { padding: .8rem 1.2rem; }
.card-meta  { color: #64748b; font-size: .82rem; display: block; }
.card-link  { color: #2563eb; font-size: .85rem; font-weight: 500; display: block; margin-top: .4rem; }
.gallery-empty { text-align: center; color: #64748b; padding: 3rem 0; font-size: .95rem; }

.inner-wrap { max-width: 760px; margin: 0 auto; padding: 2.5rem 1.5rem 4rem; }
.inner-wrap h1 { color: #0f172a; font-size: 1.8rem; font-weight: 800; margin-bottom: .4rem; }
.inner-wrap .subtitle { color: #64748b; margin-bottom: 1.5rem; }
hr.inner-divider { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
</style>
"""


def inject_styles():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_header():
    _html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:60px;overflow:hidden;background:#ffffff}
header{
  height:60px;width:100%;display:flex;align-items:center;padding:0 2.5rem;
  background:#ffffff;border-bottom:1px solid #e5e7eb;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  position:relative;
}
.logo{font-size:1.4rem;font-weight:800;color:#0f172a;
  cursor:pointer;letter-spacing:.1em;user-select:none;flex-shrink:0}
.logo:hover{color:#2563eb}
nav{position:absolute;left:50%;transform:translateX(-50%);white-space:nowrap}
nav span{margin:0 .9rem;font-size:.9rem;font-weight:500;
  color:#4b5563;cursor:pointer;user-select:none}
nav span:hover{color:#2563eb}
</style>
</head>
<body>
<header>
  <span class="logo" onclick="go('/')">KOJO</span>
  <nav>
    <span onclick="go('/')">ホーム</span>
    <span onclick="go('/upload')">動画を投稿</span>
  </nav>
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
// data-nav クリックハンドラ（hero・card用）
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
    // data-filter select changeハンドラ（フィルター用）
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
// iframeコンテナを fixed ヘッダーとして固定
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
</html>"""
    try:
        _src = "data:text/html;base64," + base64.b64encode(_html.encode()).decode()
        st.iframe(_src, height=60, scrolling=False)
    except AttributeError:
        import streamlit.components.v1 as components
        components.html(_html, height=60, scrolling=False)
