from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Temporarily allow all origins (for development/Shopify preview)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# --- simple product catalog (expand later) -----------------
PRODUCTS = [
    # Snoring
    {"tag": "sleep", "name": "Anti-Snore Chin Strap", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/snore_chinstrap", "blurb": "Comfortably keeps your mouth closed to reduce snoring."},
    {"tag": "sleep", "name": "Nasal Dilator Set", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/nasal_dilator", "blurb": "Opens nasal passages to improve breathing and reduce snoring."},

    # Confidence
    {"tag": "skin_health", "name": "Confidence Boost Journal", "image_url": "https://s.hdnux.com/photos/13/33/46/2996622/22/rawImage.jpg", "product_url": "https://yourdropshipsource.com/confidence_journal", "blurb": "Daily prompts to reinforce self-worth and personal strength."},
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

    if answers.get("Do you experience dry or flaky skin?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("skin_texture")
        if answers.get("Are you looking for a moisturizer suitable for sensitive or eczema-prone skin?") == "Yes":
            tags.append("dry_skin")
        if answers.get("Are you looking for a serum or mask that provides overnight hydration?") == "Yes":
            tags.append("hydrating_mask")

    # Acne
    if answers.get("Do you frequently deal with pimples, acne, blackheads, or clogged pores?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("skin_health")
        if answers.get("Are you interested in spot treatments or patches to reduce breakouts overnight?") == "Yes":
            tags.append("acne")
        if answers.get("Would you be open to using salicylic acid or adapalene (retinoid) treatments for acne?") == "Yes":
            tags.append("retinoid")

    # Sleep
    if answers.get("Do you have trouble falling asleep or staying asleep at night?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("sleep")
        if answers.get("Are you looking for a non-habit-forming sleep supplement?") == "Yes":
            tags.append("sleep_supplement")
        if answers.get("Are you interested in physical products (e.g., white noise machines or nasal strips) that promote better sleep?") == "Yes":
            tags.append("sleep_aids")

    # Energy
    if answers.get("Do you experience low energy or fatigue during the day?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("energy")
        if answers.get("Would you prefer gummies, capsules, or softgels for your energy supplements?") == "Yes":
            tags.append("energy_gummies")
        if answers.get("Are you looking for a caffeine-free energy booster?") == "Yes":
            tags.append("caffeine_free_energy")

    # Stress
    if answers.get("Are you looking to reduce your stress or anxiety levels?") in ["Yes", "Maybe", "Not sure"]:
        tags.append("stress")
        if answers.get("Do you prefer ashwagandha or other adaptogens for managing stress??") == "Yes":
            tags.append("ashwagandha")
        if answers.get("Would you rather take stress support in gummy or capsule form?") == "Yes":
            tags.append("stress_gummies")

    # Eye care
    if answers.get("Are your eyes dry, red, or irritated frequently??") in ["Almost daily", "Occasionally", "Not sure"]:
        tags.append("eyes")
        if answers.get("Are you interested in products that reduce puffiness or dark circles under your eyes?") == "Yes":
            tags.append("eye_care")
        if answers.get("Do you prefer eye drops or under-eye patches for your routine?") == "Yes":
            tags.append("eye_drops")

    # Hair care
    if answers.get("Do you struggle with hair loss or frizzy/dry hair?") in ["Almost daily", "Occasionally", "Not sure"]:
        tags.append("hair")
        if answers.get("Do you want to boost hair growth or thickness using supplements?") == "Yes":
            tags.append("hair_growth")
        if answers.get("Are you looking for products that improve your hair's shine and smoothness?") == "Yes":
            tags.append("hair_smoothness")

    # Minimalist
    if answers.get("Are you a minimalist who prefers a simple, low-maintenance routine?") in ["Yes", "Maybe", "Not sure"]:
        tags.append("convenient")
        if answers.get("Would you like recommendations for versatile products (e.g., facial cleansers that double as makeup removers)?") == "Yes":
            tags.append("minimalist_cleanser")
        if answers.get("Are you looking for travel-friendly or multi-use products?") == "Yes":
            tags.append("travel_friendly")

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

