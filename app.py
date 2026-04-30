import base64
import streamlit as st
from pathlib import Path
from utils.database import init_db, get_public_advice
from utils.ui import inject_styles, render_header

st.set_page_config(page_title="KOJO", page_icon="🏅", layout="wide", initial_sidebar_state="collapsed")
init_db()
inject_styles()
render_header()

_hero_bg = Path(__file__).parent / "images" / "hero_bg.webp"
if _hero_bg.exists():
    _b64 = base64.b64encode(_hero_bg.read_bytes()).decode()
    _ext = _hero_bg.suffix.lstrip(".")
    st.markdown(f"""
<style>
.hero {{
    background:
        linear-gradient(140deg, rgba(15,23,42,.2) 0%, rgba(30,58,95,.2) 60%, rgba(22,78,99,.2) 100%),
        url("data:image/{_ext};base64,{_b64}") center/cover no-repeat;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<section class="hero">
    <h1>KOJO</h1>
    <p>AIがあなたの動画を分析して、<br><b>上達のアドバイス</b>と<b>練習メニュー</b>を提供します。</p>
    <a class="hero-btn" data-nav="/upload">動画でアドバイスと練習メニューをもらう</a>
</section>
""", unsafe_allow_html=True)

public_advice = get_public_advice()


def _img_src(thumb_path: str) -> str:
    p = Path(thumb_path) if thumb_path else None
    if p and p.exists():
        b64 = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/jpeg;base64,{b64}"
    return "https://placehold.co/320x180/64748b/ffffff?text=No+Thumbnail"


if not public_advice:
    st.markdown("""
    <section class="gallery-section">
        <h2>みんながもらったアドバイス</h2>
        <p class="gallery-empty">まだ公開されているアドバイスはありません。<br>最初のアドバイスを投稿してみましょう！</p>
    </section>
    """, unsafe_allow_html=True)
else:
    sport_filter = st.query_params.get("sport", "")
    age_filter   = st.query_params.get("age", "")

    sports = sorted(set(a["sport"] for a in public_advice))
    ages   = sorted(set(a["age"]   for a in public_advice))

    # フィルター適用
    filtered = [
        a for a in public_advice
        if (not sport_filter or a["sport"] == sport_filter)
        and (not age_filter or str(a["age"]) == age_filter)
    ]

    # スポーツ選択肢
    sport_opts = '<option value="">すべてのスポーツ</option>' + "".join(
        f'<option value="{s}"{"selected" if s == sport_filter else ""}>{s}</option>'
        for s in sports
    )
    # 年齢選択肢
    age_opts = '<option value="">すべての年齢層</option>' + "".join(
        f'<option value="{age}"{"selected" if age == age_filter else ""}>{age}</option>'
        for age in ages
    )

    # カード生成
    if filtered:
        cards = "".join(
            f'<a class="card" data-nav="/detail?id={a["id"]}">'
            f'<div class="card-thumb">'
            f'<img src="{_img_src(a.get("thumbnail_path",""))}" alt="サムネール">'
            f'<div class="card-thumb-overlay">'
            f'<span class="overlay-sport">{a["sport"]}</span>'
            f'<span class="overlay-age">{a["age"]}</span>'
            f'</div></div>'
            f'<div class="card-body">'
            f'<span class="card-meta">{a["created_at"][:10]}</span>'
            f'<span class="card-link">詳細を見る →</span>'
            f'</div></a>'
            for a in filtered
        )
        grid = f'<div class="card-grid">{cards}</div>'
    else:
        grid = '<p class="gallery-empty">条件に一致するアドバイスがありません。</p>'

    st.markdown(
        f'<section class="gallery-section">'
        f'<h2>みんながもらったアドバイス</h2>'
        f'<div class="filter-box">'
        f'<span class="filter-label">絞り込み</span>'
        f'<div class="filter-bar">'
        f'<select data-filter="sport">{sport_opts}</select>'
        f'<select data-filter="age">{age_opts}</select>'
        f'</div>'
        f'</div>'
        f'{grid}'
        f'</section>',
        unsafe_allow_html=True,
    )
