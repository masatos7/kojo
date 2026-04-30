import streamlit as st
from utils.database import init_db, insert_advice
from utils.video_utils import save_uploaded_video, extract_thumbnail
from utils.gemini_client import analyze_video
from utils.ui import inject_styles, render_header

st.set_page_config(page_title="動画を投稿 | KOJO", page_icon="📹", layout="wide", initial_sidebar_state="collapsed")
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
    padding-bottom: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h2>動画でアドバイスをもらう</h2>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">動画をアップロードすると、AIがフォームや技術を分析して具体的なアドバイスを提供します。</p>', unsafe_allow_html=True)
st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

SPORTS = ["サッカー", "野球", "短距離走（かけっこ）", "長距離走（マラソン）", "逆上がり", "ゴルフ", "トランポリン", "体操", "ダンス", "ピアノ", "ギター"]
AGE_LABELS = ["未就学児", "小学生", "中学生", "高校生", "大学生", "社会人"]

with st.form("upload_form"):
    sport = st.selectbox("スポーツを選択", SPORTS)
    age = st.selectbox("年齢層を選択", AGE_LABELS)
    video_file = st.file_uploader(
        "動画ファイルをアップロード",
        type=["mp4", "mov", "avi", "webm", "mkv"],
        help="最大 200MB まで対応しています",
    )
    is_public = st.radio(
        "公開設定",
        ["公開（みんなに見せる）", "非公開（自分だけ）"],
        index=0,
    )
    submitted = st.form_submit_button("AIに分析してもらう 🚀", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    if video_file is None:
        st.error("動画ファイルを選択してください。")
        st.stop()

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error("Gemini API キーが設定されていません。`.streamlit/secrets.toml` に `GEMINI_API_KEY` を設定してください。")
        st.stop()

    with st.spinner("動画を保存中..."):
        video_path = save_uploaded_video(video_file)
        thumbnail_path = extract_thumbnail(video_path)

    with st.spinner("AIが動画を分析中です。しばらくお待ちください...（1〜2分かかる場合があります）"):
        try:
            advice_text, practice_menu = analyze_video(
                api_key=api_key,
                video_path=video_path,
                sport=sport,
                age_label=age,
            )
        except Exception as e:
            st.error(f"分析中にエラーが発生しました: {e}")
            st.stop()

    public_flag = is_public.startswith("公開")
    advice_id = insert_advice(
        sport=sport,
        age=age,
        video_path=video_path,
        thumbnail_path=thumbnail_path,
        advice_text=advice_text,
        practice_menu=practice_menu,
        is_public=public_flag,
    )

    st.session_state["advice_id"] = advice_id
    st.switch_page("pages/detail.py")
