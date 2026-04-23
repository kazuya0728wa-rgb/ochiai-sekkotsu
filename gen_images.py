"""おちあい整骨院 画像生成 (A2アンカー方式)"""
import os, json
from google import genai
from google.genai import types

CRED_FILE = os.path.expanduser("~/.claude/credentials/services/gemini.json")
OUT = "C:/tmp/ochiai-sekkotsu/images"
os.makedirs(OUT, exist_ok=True)

with open(CRED_FILE) as f:
    key = json.load(f)["credentials"]["API_KEY"]
client = genai.Client(api_key=key)

# アンカー: つかもと接骨院で確立したフラットベクタースタイル
ANCHOR_PATH = "C:/tmp/tsukamoto-sekkotsu/images/service_physical.png"
with open(ANCHOR_PATH, "rb") as f:
    anchor_bytes = f.read()
anchor = types.Part.from_bytes(data=anchor_bytes, mime_type="image/png")

ANCHOR_STYLE = (
    "Draw in EXACTLY the same illustration style as the reference image: "
    "same clean flat vector illustration style, same smooth line weight, "
    "same proportional modern character design (not exaggerated), "
    "same soft pastel color palette, same clean white or very light background, "
    "same professional medical illustration aesthetic — adult and polished, not childish. "
    "NO thick dark outlines. NO cartoon exaggeration. NO sketchy lines. "
    "Subtle background elements (floor shadow, simple furniture) rather than pure white. "
    "No text, no labels anywhere."
)

def gen(prompt, name, label):
    print(f"[gen] {label}")
    txt = types.Part(text=f"{ANCHOR_STYLE} New scene: {prompt}")
    resp = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=types.Content(parts=[anchor, txt]),
        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
    )
    for p in resp.candidates[0].content.parts:
        if p.inline_data:
            path = f"{OUT}/{name}"
            with open(path, "wb") as f:
                f.write(p.inline_data.data)
            print(f"  ✓ {name} ({os.path.getsize(path)//1024}KB)")
            return True
    print(f"  ✗ no image for {name}")
    return False

# 1. 一般施術（手技療法）
gen(
    "professional therapist performing gentle hands-on manual therapy on patient's lower back, "
    "patient lying face-down on treatment table, therapist's hands pressing gently on lumbar area, "
    "clinic treatment room background with treatment table and curtains",
    "service_general.png", "一般施術"
)

# 2. 交通事故施術
gen(
    "professional therapist gently treating patient's neck with hands, patient seated on treatment chair, "
    "therapist standing behind applying gentle cervical mobilization, clinic background",
    "service_accident.png", "交通事故施術"
)

# 3. 酸素カプセルイラスト
gen(
    "modern oval oxygen capsule pod machine in clean clinic setting, soft teal and white color scheme, "
    "capsule open showing comfortable interior padding, subtle clinic room background, "
    "clean modern medical equipment illustration",
    "service_oxygen.png", "酸素カプセル"
)

# 4. 交通事故相談イメージ（ac_kokoroe差し替え）
gen(
    "adult woman sitting in car driver seat, touching neck with concerned expression after minor collision, "
    "car interior background with slight crumple indication, calm and professional illustration",
    "accident_scene.png", "交通事故シーン"
)

# 5. 相談・問い合わせイメージ（ac_onayami差し替え）
gen(
    "friendly professional therapist in white uniform sitting at desk consulting with patient, "
    "patient looks relieved, clipboard on desk, warm clinic consultation room background",
    "accident_consult.png", "交通事故相談"
)

# 6. 回復したグループ（gr_img1差し替え）
gen(
    "group of three adults — middle-aged man, elderly woman, young man — all smiling and looking energetic, "
    "giving thumbs up, casual indoor setting, conveying health and vitality after successful treatment",
    "recovery_group.png", "回復グループ"
)

# 7. スポーツ施術（スポーツトレーナー活動あり）
gen(
    "sports trainer applying kinesiology tape to athlete's knee, athlete wearing sports uniform sitting on bench, "
    "sports gym background, professional athletic injury prevention scene",
    "service_sports.png", "スポーツ施術"
)

print("\n全生成完了")
