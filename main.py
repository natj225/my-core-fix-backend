from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Temporarily allow all origins (for development/Shopify preview)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# --- simple product catalog (expand later) -----------------
PRODUCTS = [
    # Snoring
    {"tag": "snoring", "name": "Anti-Snore Chin Strap", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/snore_chinstrap", "blurb": "Comfortably keeps your mouth closed to reduce snoring."},
    {"tag": "snoring", "name": "Nasal Dilator Set", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/nasal_dilator", "blurb": "Opens nasal passages to improve breathing and reduce snoring."},

    # Confidence
    {"tag": "confidence", "name": "Confidence Boost Journal", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/confidence_journal", "blurb": "Daily prompts to reinforce self-worth and personal strength."},
    {"tag": "confidence", "name": "Posture Enhancer Tape", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/posture_tape", "blurb": "Improves appearance and posture for a more confident look."},

    # Energy
    {"tag": "energy", "name": "Natural Energy Gummies", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/energy_gummies", "blurb": "B12 and green tea extract for clean, lasting energy."},
    {"tag": "energy", "name": "Adaptogen Energy Mix", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/energy_mix", "blurb": "Adaptogenic herbs to support energy without the crash."},

    # Skin
    {"tag": "skin", "name": "Hydrating Face Mask", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/face_mask", "blurb": "Botanical hydration for irritated or acne-prone skin."},
    {"tag": "skin", "name": "Skin Renewal Serum", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/serum", "blurb": "Supports clear skin with vitamin C and niacinamide."},

    # Social
    {"tag": "social", "name": "Social Ease Gummies", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/social_gummies", "blurb": "Blend of calming herbs to reduce tension in social settings."},
    {"tag": "social", "name": "Pocket Affirmation Cards", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/affirmations", "blurb": "Positive reinforcement on the go to calm the mind."},

    # Productivity
    {"tag": "productivity", "name": "Daily Habit Tracker", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/habit_tracker", "blurb": "Build habits and stay accountable daily."},
    {"tag": "productivity", "name": "Focus Timer Cube", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/focus_cube", "blurb": "Boosts focus using the Pomodoro method with a physical cube."},

    # Stress
    {"tag": "stress", "name": "Ashwagandha Gummies", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/ashwagandha", "blurb": "Reduces cortisol and stress naturally."},
    {"tag": "stress", "name": "Calming Weighted Wrap", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/weighted_wrap", "blurb": "Provides a grounding sensation to reduce stress and anxiety."},

    # Caffeine / Fatigue
    {"tag": "caffeine", "name": "Caffeine-Free Energy Boost", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/caffeine_free_energy", "blurb": "Stay energized without relying on caffeine."},
    {"tag": "caffeine", "name": "Morning Wake-Up Light", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/wakeup_light", "blurb": "Simulates natural sunlight to start your day."},

    # Journaling
    {"tag": "journaling", "name": "Self-Therapy Journal", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/therapy_journal", "blurb": "Guided journal to improve self-awareness and clarity."},
    {"tag": "journaling", "name": "Mood Tracker Notebook", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/mood_tracker", "blurb": "Track your emotions and recognize patterns over time."}
]

def assign_tags(answers):
    tags = []

    if answers.get("Do you or your partner notice snoring?") == "Yes":
        tags.append("snoring")
    if answers.get("How often do you feel confident in your appearance?") == "Never":
        tags.append("confidence")
    if answers.get("Do you experience low energy throughout the day?") == "Yes":
        tags.append("energy")
    if answers.get("How well do you typically sleep at night?") == "Poorly":
        tags.append("skin")
    if answers.get("Do you follow a regular daily routine?") == "Not really":
        tags.append("social")
    if answers.get("How often do you feel overwhelmed or stressed?") == "Almost daily":
        tags.append("productivity")
    if answers.get("How would you describe your skin health?") == "Problematic":
        tags.append("stress")
    if answers.get("Do you feel mentally sharp and focused?") == "Rarely":
        tags.append("caffeine")
    if answers.get("How frequently do you exercise or move your body?") == "Never":
        tags.append("journaling")
    if answers.get("Do you rely on caffeine to get through your day?") == "Yes":
        tags.append("journaling")

    return tags

def match_products(tags):
    return [product for product in PRODUCTS if product["tag"] in tags]

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    answers = data.get("answers", {})
    free_text = data.get("free_text", "")
    tags = assign_tags(answers)
    matched_products = match_products(tags)
    return jsonify({"tags": tags, "products": matched_products})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

