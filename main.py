from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Temporarily allow all origins (for development/Shopify preview)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# --- simple product catalog (expand later) -----------------
PRODUCTS = [
    # Snoring
     {
    "tag": "face-care",
    "name": "Aloe Rose Hydration Mist",
    "image_url": "https://mycorefix.com/cdn/shop/files/61gkFcU2s7L._SL1500.jpg",
    "product_url": "",
    "blurb": "Refreshing face spray with aloe, rosewater, and botanicals to hydrate and revive skin.",
    "variant_id": "43254188572732",
    "price": 7.73,
    "benefits": [
        "Instantly hydrates skin",
        "Soothes redness and irritation",
        "Suitable for all skin types"
        ]
  }

]

def assign_tags(answers):
    tags = []

    if answers.get("Do you experience dry or flaky skin?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("repair-moisturizer")
        if answers.get("Are you looking for a moisturizer suitable for sensitive or eczema-prone skin?") == "Yes":
            tags += ["face-towels", "snail-nut", "prebiotic-lotion", "jelly-hydration"]
        if answers.get("Are you looking for a serum or mask that provides overnight hydration?") == "Yes":
            tags += ["snail-nut", "purifying-gel", "collagen-mask", "deep-mask", "aloe-face"]

    # Acne
    if answers.get("Do you frequently deal with pimples, acne, blackheads, or clogged pores?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("daily-scrub")
        if answers.get("Are you interested in spot treatments or patches to reduce breakouts overnight?") == "Yes":
            tags += ["purifying-gel", "acne-patch", "spot-gel"]
        if answers.get("Would you be open to using salicylic acid or adapalene (retinoid) treatments for acne?") == "Yes":
            tags += ["2-bha", "adapalene-acne", "spot-gel"]
    # Sleep
    if answers.get("Do you have trouble falling asleep or staying asleep at night?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("mouth-tape")
        if answers.get("Are you looking for a non-habit-forming sleep supplement?") == "Yes":
            tags += ["sleeptabs-night", "melatonin-magnesium"]
        if answers.get("Are you interested in physical products (e.g., white noise machines or nasal strips) that promote better sleep?") == "Yes":
            tags += ["nasal-strips", "white-machine"]

    # Energy
    if answers.get("Do you experience low energy or fatigue during the day?") in ["Yes", "Sometimes", "Not sure"]:
        tags.append("ginkgo-biloba")
        if answers.get("Would you prefer gummies, capsules, or softgels for your energy supplements?") == "Yes":
            tags += ["b12-supplement", "caffeine-gummies", "apple-cider"]
        if answers.get("Are you looking for a caffeine-free energy booster?") == "Yes":
            tags += ["caffeine-gummies", "apple-cider", "alpha-brain"]

    # Stress
    if answers.get("Are you looking to reduce your stress or anxiety levels?") in ["Yes", "Maybe", "Not sure"]:
        if answers.get("Do you prefer ashwagandha or other adaptogens for managing stress??") == "Yes":
            tags += ["pure-ash", "ash-d"]
        if answers.get("Would you rather take stress support in gummy or capsule form?") == "Yes":
            tags += ["pure-ash", "ash-d"]

    # Eye care
    if answers.get("Are your eyes dry, red, or irritated frequently??") in ["Almost daily", "Occasionally", "Not sure"]:
        if answers.get("Are you interested in products that reduce puffiness or dark circles under your eyes?") == "Yes":
            tags += ["50-vision", "gold-mask"]
        if answers.get("Do you prefer eye drops or under-eye patches for your routine?") == "Yes":
            tags += ["gold-mask", "redness-relief"]

    # Hair care
    if answers.get("Do you struggle with hair loss or frizzy/dry hair?") in ["Almost daily", "Occasionally", "Not sure"]:
        tags.append("bio-skin")
        if answers.get("Do you want to boost hair growth or thickness using supplements?") == "Yes":
            tags += ["liquid-biotin", "keratin-boost"]
        if answers.get("Are you looking for products that improve your hair's shine and smoothness?") == "Yes":
            tags += ["glossing-hair", "dream-coat", "liquid-biotin"]

    # Minimalist
    if answers.get("Are you a minimalist who prefers a simple, low-maintenance routine?") in ["Yes", "Maybe", "Not sure"]:
        tags.append("foaming-body")
        if answers.get("Would you like recommendations for versatile products (e.g., facial cleansers that double as makeup removers)?") == "Yes":
            tags += ["contact-solution", "pink-tape", "micropore-tape", "coco-nut"]
        if answers.get("Are you looking for travel-friendly or multi-use products?") == "Yes":
            tags += ["contact-solution", "pink-tape", "micropore-tape", "plum-lip"]

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

