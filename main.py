from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Add this line

app = Flask(__name__)
CORS(app)  # 👈 Add this line

# --- simple product catalog (expand later) -----------------
PRODUCTS = [
    # Sleep Issues
    {"tag": "sleep_issues", "name": "Deep Sleep Pillow Spray", "image_url": "https://cdn.com/sleep_spray.png", "product_url": "https://yourdropshipsource.com/sleep_spray", "blurb": "Clinically proven to help you fall asleep faster and wake up refreshed."},
    {"tag": "sleep_issues", "name": "Smart Sleep Mask", "image_url": "https://cdn.com/smart_sleep_mask.png", "product_url": "https://yourdropshipsource.com/smart_sleep_mask", "blurb": "Blocks out light and emits calming sounds to enhance deep sleep."},

    # Snoring
    {"tag": "snoring", "name": "Anti-Snore Chin Strap", "image_url": "https://cdn.com/snore_chinstrap.png", "product_url": "https://yourdropshipsource.com/snore_chinstrap", "blurb": "Comfortably keeps your mouth closed to reduce snoring."},
    {"tag": "snoring", "name": "Nasal Dilator Set", "image_url": "https://cdn.com/nasal_dilator.png", "product_url": "https://yourdropshipsource.com/nasal_dilator", "blurb": "Opens nasal passages to improve breathing and reduce snoring."},

    # Confidence
    {"tag": "confidence", "name": "Confidence Boost Journal", "image_url": "https://cdn.com/confidence_journal.png", "product_url": "https://yourdropshipsource.com/confidence_journal", "blurb": "Daily prompts to reinforce self-worth and personal strength."},
    {"tag": "confidence", "name": "Posture Enhancer Tape", "image_url": "https://cdn.com/posture_tape.png", "product_url": "https://yourdropshipsource.com/posture_tape", "blurb": "Improves appearance and posture for a more confident look."},

    # Energy Levels
    {"tag": "energy", "name": "Natural Energy Gummies", "image_url": "https://cdn.com/energy_gummies.png", "product_url": "https://yourdropshipsource.com/energy_gummies", "blurb": "B12 and green tea extract for clean, lasting energy."},
    {"tag": "energy", "name": "Adaptogen Energy Mix", "image_url": "https://cdn.com/energy_mix.png", "product_url": "https://yourdropshipsource.com/energy_mix", "blurb": "Adaptogenic herbs to support energy without the crash."},

    # Skin Health
    {"tag": "skin", "name": "Hydrating Face Mask", "image_url": "https://cdn.com/face_mask.png", "product_url": "https://yourdropshipsource.com/face_mask", "blurb": "Botanical hydration for irritated or acne-prone skin."},
    {"tag": "skin", "name": "Skin Renewal Serum", "image_url": "https://cdn.com/serum.png", "product_url": "https://yourdropshipsource.com/serum", "blurb": "Supports clear skin with vitamin C and niacinamide."},

    # Productivity
    {"tag": "productivity", "name": "Daily Habit Tracker", "image_url": "https://cdn.com/habit_tracker.png", "product_url": "https://yourdropshipsource.com/habit_tracker", "blurb": "Build habits and stay accountable daily."},
    {"tag": "productivity", "name": "Focus Timer Cube", "image_url": "https://cdn.com/focus_cube.png", "product_url": "https://yourdropshipsource.com/focus_cube", "blurb": "Boosts focus using the Pomodoro method with a physical cube."},

    # Stress
    {"tag": "stress", "name": "Ashwagandha Gummies", "image_url": "https://cdn.com/ashwagandha.png", "product_url": "https://yourdropshipsource.com/ashwagandha", "blurb": "Reduces cortisol and stress naturally."},
    {"tag": "stress", "name": "Calming Weighted Wrap", "image_url": "https://cdn.com/weighted_wrap.png", "product_url": "https://yourdropshipsource.com/weighted_wrap", "blurb": "Provides a grounding sensation to reduce stress and anxiety."},

    # Social Anxiety
    {"tag": "social", "name": "Social Ease Gummies", "image_url": "https://cdn.com/social_gummies.png", "product_url": "https://yourdropshipsource.com/social_gummies", "blurb": "Blend of calming herbs to reduce tension in social settings."},
    {"tag": "social", "name": "Pocket Affirmation Cards", "image_url": "https://cdn.com/affirmations.png", "product_url": "https://yourdropshipsource.com/affirmations", "blurb": "Positive reinforcement on the go to calm the mind."},

    # Posture
    {"tag": "posture", "name": "Posture Corrector Band", "image_url": "https://cdn.com/posture_band.png", "product_url": "https://yourdropshipsource.com/posture_band", "blurb": "Encourages upright posture and reduces strain on your back."},
    {"tag": "posture", "name": "Ergonomic Lumbar Cushion", "image_url": "https://cdn.com/lumbar_cushion.png", "product_url": "https://yourdropshipsource.com/lumbar_cushion", "blurb": "Supports your lower back while sitting for long hours."},

    # Journaling / Mental Wellness
    {"tag": "journaling", "name": "Self-Therapy Journal", "image_url": "https://cdn.com/therapy_journal.png", "product_url": "https://yourdropshipsource.com/therapy_journal", "blurb": "Guided journal to improve self-awareness and clarity."},
    {"tag": "journaling", "name": "Mood Tracker Notebook", "image_url": "https://cdn.com/mood_tracker.png", "product_url": "https://yourdropshipsource.com/mood_tracker", "blurb": "Track your emotions and recognize patterns over time."}
]
# ---------- helper functions --------------------------------
def assign_tags(answers: dict) -> list[str]:
    """Return a list of product-tags based on survey answers."""
    tags = []
    if answers.get("How well do you sleep most nights?") == "I struggle to fall or stay asleep":
        tags.append("sleep_aid")
    if answers.get("How often do you feel confident in yourself or your appearance?") == "Rarely":
        tags.append("confidence_boost")
    return tags

def match_products(tags: list[str]) -> list[dict]:
    """Return product dicts whose tag is in tags list."""
    return [p for p in PRODUCTS if p["tag"] in tags]

# --------------- API endpoint --------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    # Expect simple payload: { "answers": { question: answer, … } }
    answers = data.get("answers", {})
    tags = assign_tags(answers)
    products = match_products(tags)

    return jsonify({"tags": tags, "products": products})

# ----------------- local run ---------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
