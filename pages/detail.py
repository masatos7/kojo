import streamlit as st
from pathlib import Path
from utils.database import init_db, get_advice_by_id
from utils.ui import inject_styles, render_header

st.set_page_config(page_title="アドバイス詳細 | KOJO", page_icon="🏅", layout="wide", initial_sidebar_state="collapsed")
init_db()
inject_styles()
render_header()
st.markdown("""
<style>
[data-testid="stMainBlockContainer"] {
    max-width: 820px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    padding-bottom: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# URL クエリパラメータ → セッション → フォールバック
advice_id = st.query_params.get("id") or st.session_state.get("advice_id")

if not advice_id:
    st.warning("アドバイスが選択されていません。")
    if st.button("ホームへ戻る"):
        st.switch_page("app.py")
    st.stop()

advice = get_advice_by_id(int(advice_id))
if not advice:
    st.error("指定されたアドバイスが見つかりませんでした。")
    if st.button("ホームへ戻る"):
        st.switch_page("app.py")
    st.stop()


st.markdown(f'<h2>🏅 {advice["sport"]} のアドバイス</h2>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">対象: {advice["age"]} · 投稿日: {advice["created_at"][:10]}</p>', unsafe_allow_html=True)
st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

# 動画
video_path = advice.get("video_path", "")
if video_path and Path(video_path).exists():
    st.subheader("アップロード動画")
    with open(video_path, "rb") as f:
        st.video(f.read())

# アドバイス
st.subheader("アドバイス")
advice_text = advice.get("advice_text") or ""
if advice_text:
    st.markdown(advice_text)
else:
    st.info("アドバイスがありません。")

st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

# 練習メニュー
st.subheader("📋 練習メニュー")
practice_menu = advice.get("practice_menu") or ""
if practice_menu:
    st.markdown(practice_menu)
else:
    st.info("練習メニューがありません。")

st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

if st.button("← ホームへ戻る"):
    st.switch_page("app.py")

st.markdown('</div>', unsafe_allow_html=True)
