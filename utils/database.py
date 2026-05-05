import streamlit as st


def _sb():
    from supabase import create_client
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SERVICE_KEY"])


def init_db():
    pass  # テーブルは Supabase ダッシュボードで作成済み


def insert_advice(sport, age, video_path, thumbnail_path, advice_text, practice_menu, is_public):
    result = _sb().table("advice").insert({
        "sport": sport,
        "age": age,
        "video_path": str(video_path),
        "thumbnail_path": str(thumbnail_path),
        "advice_text": advice_text,
        "practice_menu": practice_menu,
        "is_public": bool(is_public),
    }).execute()
    return result.data[0]["id"]


def get_public_advice():
    result = _sb().table("advice").select("*").eq("is_public", True).order("created_at", desc=True).execute()
    return result.data


def get_advice_by_id(advice_id):
    result = _sb().table("advice").select("*").eq("id", advice_id).execute()
    return result.data[0] if result.data else None


def get_all_advice():
    result = _sb().table("advice").select("*").order("created_at", desc=True).execute()
    return result.data


def delete_advice(advice_id):
    _sb().table("advice").delete().eq("id", advice_id).execute()
