import time
from pathlib import Path
import google.generativeai as genai

SPORT_LABELS = {
    "サッカー": "サッカー",
    "野球": "野球",
    "短距離走（かけっこ）": "短距離走",
    "長距離走（マラソン）": "長距離走・マラソン",
    "逆上がり": "逆上がり（鉄棒）",
    "ゴルフ": "ゴルフ",
    "トランポリン": "トランポリン",
    "体操": "体操",
    "ダンス": "ダンス",
    "ピアノ": "ピアノ",
    "ギター": "ギター",
}

PROMPTS = {
    "サッカー": "ドリブル・パス・シュート・ポジショニングなどの技術面とフォームを中心に分析してください。",
    "野球": "バッティングフォーム・ピッチングフォーム・守備の動作を中心に分析してください。",
    "短距離走（かけっこ）": "スタートの姿勢、腕振り、足の接地・蹴り出しフォームを中心に分析してください。",
    "長距離走（マラソン）": "フォーム効率・ペース配分・呼吸法・疲労箇所を中心に分析してください。",
    "逆上がり": "踏み切り・腰の引き付け・腕の引き付け・回転のタイミング・着地姿勢を中心に分析してください。",
    "ゴルフ": "グリップ・アドレス・バックスイング・インパクト・フォロースルーのフォームを中心に分析してください。",
    "トランポリン": "踏み切りのタイミング・空中姿勢・着地バランス・技の完成度を中心に分析してください。",
    "体操": "基本姿勢・柔軟性・バランス・技の完成度・着地の安定性を中心に分析してください。",
    "ダンス": "リズム感・身体の使い方・表現力・振り付けの正確さ・重心の安定を中心に分析してください。",
    "ピアノ": "手のフォーム・指使い・リズム・姿勢・ペダリングを中心に分析してください。",
    "ギター": "右手のピッキング・左手の押弦フォーム・コードチェンジのスムーズさ・リズム・姿勢を中心に分析してください。",
}

LANGUAGE_HINTS = {
    "未就学児": (
        "回答はすべてひらがなだけでかいてください。かたかなもかんじもつかわないでください。"
        "むずかしいことばはつかわず、3〜5さいのこどもにわかるやさしいことばでせつめいしてください。"
        "よいところをかならず1〜2つほめてください。"
        "しかし、ほめるだけでなく「もっとうまくなるためのアドバイス」をかならず2〜3つ、"
        "こどもがじっさいにれんしゅうできるようにやさしくせつめいしてください。"
        "「〜してみよう！」「〜をいしきしてみよう！」など、まえむきなことばでつたえてください。"
    ),
    "小学生": (
        "小学生にわかりやすいことばで書いてください。"
        "むずかしい漢字にはふりがなをつけてください。"
        "専門用語は使わず、身近なたとえを交えてわかりやすく説明してください。"
        "前向きで楽しい言葉づかいを心がけてください。"
    ),
}


def analyze_video(api_key: str, video_path: Path, sport: str, age_label: str) -> tuple[str, str]:
    genai.configure(api_key=api_key)

    # 動画をアップロード
    video_file = genai.upload_file(str(video_path))
    while video_file.state.name == "PROCESSING":
        time.sleep(3)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise RuntimeError("動画のアップロードに失敗しました。")

    sport_label = SPORT_LABELS.get(sport, sport)
    sport_hint = PROMPTS.get(sport, "")
    language_hint = LANGUAGE_HINTS.get(age_label, "")

    prompt = f"""あなたは{sport_label}の経験豊富なプロコーチです。
この動画を見て、{age_label}のプレイヤーに対して具体的なフィードバックを日本語で提供してください。
{sport_hint}
{language_hint}

以下の形式で必ず回答してください：

---
## アドバイス

（動画で確認できた良い点と改善すべき点を、それぞれ箇条書きで3〜5点ずつ具体的に記述）

---
## 練習メニュー

（このプレイヤーの課題を克服するための練習ドリルを3〜5つ提案してください。
各ドリルには名前・目的・具体的なやり方・推奨時間を記載してください）

---
"""

    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content([video_file, prompt])

    full_text = response.text
    # アドバイスと練習メニューを分割
    if "## 練習メニュー" in full_text:
        parts = full_text.split("## 練習メニュー", 1)
        advice_text = parts[0].replace("## アドバイス", "").strip().strip("---").strip()
        practice_menu = parts[1].strip().strip("---").strip()
    else:
        advice_text = full_text
        practice_menu = ""

    return advice_text, practice_menu
