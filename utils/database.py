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


def get_all_guides():
    result = _sb().table("sport_guides").select("sport").execute()
    return [r["sport"] for r in result.data]


def get_guide_by_sport(sport):
    result = _sb().table("sport_guides").select("*").eq("sport", sport).execute()
    return result.data[0] if result.data else None


def upsert_guide(sport, common_mistakes, practice_methods, tips):
    _sb().table("sport_guides").upsert({
        "sport": sport,
        "common_mistakes": common_mistakes,
        "practice_methods": practice_methods,
        "tips": tips,
    }, on_conflict="sport").execute()
