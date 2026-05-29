"""
スポーツガイドを Gemini で生成して Supabase に保存するスクリプト。
プロジェクトルートから実行: python scripts/generate_guides.py

事前に Supabase で以下のテーブルを作成してください:

  create table sport_guides (
    id          bigserial primary key,
    sport       text unique not null,
    common_mistakes  text,
    practice_methods text,
    tips        text,
    created_at  timestamptz default now()
  );
"""

import sys
import time
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # Python < 3.11

sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from supabase import create_client

SPORTS = [
    "サッカー",
    "野球",
    "短距離走（かけっこ）",
    "長距離走（マラソン）",
    "逆上がり",
    "跳び箱",
    "ゴルフ",
    "トランポリン",
    "体操",
    "ダンス",
    "ピアノ",
    "ギター",
]


def load_secrets():
    secrets_path = Path(__file__).parent.parent / ".streamlit" / "secrets.toml"
    with open(secrets_path, "rb") as f:
        return tomllib.load(f)


def _generate_with_retry(model, prompt: str, max_retries: int = 3):
    delay = 5
    for attempt in range(max_retries + 1):
        try:
            return model.generate_content(prompt)
        except ResourceExhausted:
            if attempt >= max_retries:
                raise
            print(f"レート制限。{delay}秒後にリトライ ({attempt + 1}/{max_retries})...")
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("到達不能")


def generate_guide(model, sport: str) -> tuple[str, str, str]:
    prompt = f"""あなたは{sport}の経験豊富なプロコーチです。
{sport}の上達を目指す人向けに、実用的なガイドを日本語で作成してください。

以下の形式で必ず回答してください：

---
## よくあるミス

（初心者・中級者がやりがちなミスを5つ、それぞれ具体的な理由・影響と合わせて箇条書きで）

---
## 効果的な練習方法

（すぐ実践できる練習ドリルを5つ提案してください。各練習に「**名前**」「目的」「やり方」「推奨時間」を記載）

---
## 上達のコツ

（上達を加速させる心がけや考え方を5つ、箇条書きで）

---
"""
    response = _generate_with_retry(model, prompt)
    text = response.text

    def extract(section: str) -> str:
        marker = f"## {section}"
        if marker not in text:
            return ""
        start = text.index(marker) + len(marker)
        rest = text[start:]
        # 次のセクション手前まで
        next_pos = len(rest)
        for other in ["よくあるミス", "効果的な練習方法", "上達のコツ"]:
            if other != section:
                m = f"## {other}"
                if m in rest:
                    next_pos = min(next_pos, rest.index(m))
        return rest[:next_pos].strip().strip("---").strip()

    return (
        extract("よくあるミス"),
        extract("効果的な練習方法"),
        extract("上達のコツ"),
    )


def main():
    secrets = load_secrets()
    genai.configure(api_key=secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    sb = create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_SERVICE_KEY"])

    for sport in SPORTS:
        print(f"生成中: {sport} ...", end=" ", flush=True)
        try:
            mistakes, methods, tips = generate_guide(model, sport)
            sb.table("sport_guides").upsert({
                "sport": sport,
                "common_mistakes": mistakes,
                "practice_methods": methods,
                "tips": tips,
            }, on_conflict="sport").execute()
            print("完了")
        except Exception as e:
            print(f"エラー: {e}")
        time.sleep(10)  # RPM対策（2秒では短すぎるため）

    print("\n全スポーツのガイド生成が完了しました。")


if __name__ == "__main__":
    main()
