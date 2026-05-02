import streamlit as st
from utils.database import init_db, get_all_advice, delete_advice
from utils.video_utils import delete_from_storage
from utils.ui import inject_styles, render_header

st.set_page_config(page_title="管理画面 | KOJO", page_icon="🔧", layout="wide", initial_sidebar_state="collapsed")
init_db()
inject_styles()
render_header()
st.markdown("""
<style>
[data-testid="stMainBlockContainer"] {
    max-width: 960px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# パスコード認証
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown('<h2>管理画面</h2>', unsafe_allow_html=True)
    password = st.text_input("パスコードを入力してください", type="password")
    if st.button("ログイン", type="primary"):
        try:
            correct = st.secrets["ADMIN_PASSWORD"]
        except Exception:
            st.error("`ADMIN_PASSWORD` が secrets.toml に設定されていません。")
            st.stop()
        if password == correct:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("パスコードが違います。")
    st.stop()

# 管理画面本体
st.markdown('<h2>管理画面 — 投稿一覧</h2>', unsafe_allow_html=True)
st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

if st.button("ログアウト"):
    st.session_state.admin_authenticated = False
    st.rerun()

advice_list = get_all_advice()

if not advice_list:
    st.info("投稿はまだありません。")
    st.stop()

st.markdown(f"**合計 {len(advice_list)} 件**")
st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)

for a in advice_list:
    col_info, col_btn = st.columns([5, 1])
    with col_info:
        public_label = "公開" if a["is_public"] else "非公開"
        st.markdown(
            f"**#{a['id']}** {a['sport']} / {a['age']} / {a['created_at'][:10]} "
            f"/ {'🟢 公開' if a['is_public'] else '🔒 非公開'}"
        )
    with col_btn:
        if st.button("削除", key=f"del_{a['id']}", type="secondary"):
            st.session_state[f"confirm_{a['id']}"] = True

    if st.session_state.get(f"confirm_{a['id']}"):
        st.warning(f"ID {a['id']} の投稿を削除しますか？この操作は取り消せません。")
        yes, no = st.columns(2)
        with yes:
            if st.button("はい、削除する", key=f"yes_{a['id']}", type="primary"):
                delete_from_storage(a.get("video_path", ""), "videos")
                delete_from_storage(a.get("thumbnail_path", ""), "thumbnails")
                delete_advice(a["id"])
                st.session_state.pop(f"confirm_{a['id']}", None)
                st.success(f"ID {a['id']} を削除しました。")
                st.rerun()
        with no:
            if st.button("キャンセル", key=f"no_{a['id']}"):
                st.session_state.pop(f"confirm_{a['id']}", None)
                st.rerun()

    st.markdown('<hr class="inner-divider">', unsafe_allow_html=True)
