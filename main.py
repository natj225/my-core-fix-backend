from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Add this line

app = Flask(__name__)
CORS(app)  # 👈 Add this line

# --- simple product catalog (expand later) -----------------
PRODUCTS = [
    {
        "tag": "sleep_aid",
        "name": "Sleep Reset Mist",
        "image_url": "https://cdn.com/sleepmist.png",
        "product_url": "https://yourstore.com/products/sleep-reset-mist",
        "blurb": "Helps you drift off faster and enjoy deeper sleep."
    },
    {
        "tag": "confidence_boost",
        "name": "Self-Belief Journal",
        "image_url": "https://cdn.com/journal.png",
        "product_url": "https://yourstore.com/products/self-belief-journal",
        "blurb": "Daily prompts that rebuild self-confidence."
    }
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
