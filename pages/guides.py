import streamlit as st
from utils.database import init_db, get_all_guides, get_guide_by_sport
from utils.ui import inject_styles, render_header

st.set_page_config(page_title="練習ガイド | KOJO", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
init_db()
inject_styles()
render_header()

st.markdown("""
<style>
[data-testid="stMainBlockContainer"] {
    max-width: 900px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding: 0 1.5rem 3rem !important;
}
.guide-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 1.5rem;
}
.sport-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.4rem 1rem;
    text-align: center;
    cursor: pointer;
    transition: border-color .2s, transform .15s, box-shadow .2s;
    text-decoration: none;
    color: inherit;
    display: block;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.sport-card:hover {
    border-color: #2563eb;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(37,99,235,.1);
}
.sport-card .emoji { font-size: 2.2rem; display: block; margin-bottom: .6rem; }
.sport-card .name  { font-size: .88rem; font-weight: 700; color: #0f172a; }
.guide-section-bg { background: #f8fafc; border: 1px solid #e5e7eb; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.2rem; }
.back-link { color: #2563eb; font-size: .9rem; cursor: pointer; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

SPORT_EMOJIS = {
    "サッカー": "⚽",
    "野球": "⚾",
    "短距離走（かけっこ）": "🏃",
    "長距離走（マラソン）": "🏅",
    "逆上がり": "🤸",
    "跳び箱": "📦",
    "ゴルフ": "⛳",
    "トランポリン": "🎪",
    "体操": "🤼",
    "ダンス": "💃",
    "ピアノ": "🎹",
    "ギター": "🎸",
}

selected_sport = st.query_params.get("sport", "")

# ── 詳細表示 ──────────────────────────────────────────────
if selected_sport:
    guide = get_guide_by_sport(selected_sport)
    emoji = SPORT_EMOJIS.get(selected_sport, "🏅")

    st.markdown(f'<h2>{emoji} {selected_sport} 練習ガイド</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

    if not guide:
        st.info("このスポーツのガイドはまだ生成されていません。`python scripts/generate_guides.py` を実行してください。")
    else:
        tab1, tab2, tab3 = st.tabs(["⚠️ よくあるミス", "🏋️ 効果的な練習方法", "💡 上達のコツ"])

        with tab1:
            st.markdown(guide.get("common_mistakes") or "データなし")

        with tab2:
            st.markdown(guide.get("practice_methods") or "データなし")

        with tab3:
            st.markdown(guide.get("tips") or "データなし")

    st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)
    if st.button("← ガイド一覧に戻る"):
        st.query_params.clear()
        st.rerun()

# ── 一覧表示 ──────────────────────────────────────────────
else:
    st.markdown('<h2>練習ガイド</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="color:#64748b">スポーツを選ぶと、よくあるミス・練習方法・上達のコツが確認できます。</p>', unsafe_allow_html=True)
    st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

    available = get_all_guides()

    cards = ""
    for sport, emoji in SPORT_EMOJIS.items():
        badge = "" if sport in available else '<span style="font-size:.65rem;color:#94a3b8;display:block;margin-top:.2rem">準備中</span>'
        href = f"/guides?sport={sport}" if sport in available else "#"
        cards += (
            f'<a class="sport-card" data-nav="{href}">'
            f'<span class="emoji">{emoji}</span>'
            f'<span class="name">{sport}</span>'
            f'{badge}'
            f'</a>'
        )

    st.markdown(f'<div class="guide-grid">{cards}</div>', unsafe_allow_html=True)
