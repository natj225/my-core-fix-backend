from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Temporarily allow all origins (for development/Shopify preview)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# --- simple product catalog (expand later) -----------------
const products = [
  {
    {
    "tag": "face-towels",
    "name": "Clean Towels XL Face Wipes",
    "image_url": "https://mycorefix.com/cdn/shop/files/2fc55435010ad5a8c7e1eeedae26bc6b_600x600.jpg",
    "product_url": "",
    "blurb": "Disposable, ultra-soft face towels for hygienic cleansing and gentle makeup removal.",
    "variant_id": "43309071302716",
    "price": "19.99",
    "benefits": [
      "Promotes hygienic face cleansing",
      "Gentle for sensitive skin",
      "Perfect for travel and on-the-go"
    ]
  },
  {
    "tag": "mouth-tape",
    "name": "Purple Mouth Tape (30pk)",
    "image_url": "https://mycorefix.com/cdn/shop/files/b6c556947ff4af0c23f183069e52d22e_600x600.jpg",
    "product_url": "",
    "blurb": "Hypoallergenic, gentle adhesive tape for skin protection and everyday uses.",
    "variant_id": "43290497908796",
    "price": "15.99",
    "benefits": [
      "Gentle on sensitive skin",
      "Hypoallergenic and safe",
      "Perfect for daily and medical use"
    ]
  },
  {
    "tag": "b12-supplement",
    "name": "B12 Energy Softgels (150ct)",
    "image_url": "https://mycorefix.com/cdn/shop/files/39dfe953b8bc46aa938a69de1173b07a_600x600.jpg",
    "product_url": "",
    "blurb": "Daily vitamin B12 softgels to help support energy metabolism and combat fatigue.",
    "variant_id": "43290490535996",
    "price": "11.99",
    "benefits": [
      "Boosts daily energy levels",
      "Supports healthy metabolism",
      "Easy-to-swallow softgels"
    ]
  },
  {
    "tag": "ginkgo-biloba",
    "name": "Ginkgo Memory Boost (100ct)",
    "image_url": "https://mycorefix.com/cdn/shop/files/648d2c78223fa17760286ce29529d0fa_600x600.jpg",
    "product_url": "",
    "blurb": "Ginkgo Biloba capsules to promote focus, memory, and overall cognitive function.",
    "variant_id": "43290486636604",
    "price": "10.99",
    "benefits": [
      "Enhances memory and recall",
      "Promotes mental clarity",
      "Supports brain health"
    ]
  },
  {
    "tag": "caffeine-gummies",
    "name": "Caffeine-Free Energy Gummies",
    "image_url": "https://mycorefix.com/cdn/shop/files/0355b056cfcdeeab34495004c8bd81d3_600x600.jpg",
    "product_url": "",
    "blurb": "Tasty, chewable gummies with B12 and antioxidants for natural, jitter-free energy.",
    "variant_id": "43290486571068",
    "price": "15.99",
    "benefits": [
      "Natural energy without jitters",
      "Delicious and easy to take",
      "Caffeine-free formula"
    ]
  },
  {
    "tag": "contact-solution",
    "name": "All-in-One Contact Solution",
    "image_url": "https://mycorefix.com/cdn/shop/files/7cf284ae58e8052a1c2856d00a5bd6ad_600x600.jpg",
    "product_url": "",
    "blurb": "Cleans, conditions, and disinfects contact lenses for all-day comfort.",
    "variant_id": "43318924967996",
    "price": "20.99",
    "benefits": [
      "Cleans and disinfects lenses",
      "Keeps contacts comfortable",
      "Suitable for all lens types"
    ]
  },
  {
    "tag": "50-vision",
    "name": "50+ Vision Multivitamin",
    "image_url": "https://mycorefix.com/cdn/shop/files/b7c3044ce6845be3b0edb067eacc09ca_600x600.jpg",
    "product_url": "",
    "blurb": "Eye vitamins with lutein and omega-3 for long-term ocular health and clarity.",
    "variant_id": "43318925918268",
    "price": "24.99",
    "benefits": [
      "Supports long-term eye health",
      "Rich in lutein and omega-3",
      "Formulated for 50+ adults"
    ]
  },
  {
    "tag": "gold-mask",
    "name": "Gold Eye Mask (6 Pairs)",
    "image_url": "https://mycorefix.com/cdn/shop/files/06fdddc03991b4ddcb5c8fb8bcbef1d3_600x600.jpg",
    "product_url": "",
    "blurb": "Soothing gel patches to reduce dark circles, puffiness, and fine lines under the eyes.",
    "variant_id": "43290436796476",
    "price": "11.99",
    "benefits": [
      "Reduces puffiness and dark circles",
      "Soothes and hydrates under-eyes",
      "Quick results in minutes"
    ]
  },
  {
    "tag": "redness-relief",
    "name": "8hr Redness Relief Eye Drops",
    "image_url": "https://mycorefix.com/cdn/shop/files/818c9a63df2142e0bdb246bd1fd2bb5c_600x600.jpg",
    "product_url": "",
    "blurb": "Fast-acting eye drops to relieve redness and brighten tired eyes for up to 8 hours.",
    "variant_id": "43290436304956",
    "price": "25.99",
    "benefits": [
      "Fast relief from redness",
      "Lasts up to 8 hours",
      "Brightens tired eyes"
    ]
  },
  {
    "tag": "2-bha",
    "name": "2% BHA Pore Exfoliant",
    "image_url": "https://mycorefix.com/cdn/shop/files/f633014fabba266a12c5068eaef62b72_600x600.jpg",
    "product_url": "",
    "blurb": "Salicylic acid exfoliant to clear pores, minimize blackheads, and smooth skin.",
    "variant_id": "43290413039676",
    "price": "39.99",
    "benefits": [
      "Clears and refines pores",
      "Minimizes blackheads",
      "Smooths skin texture"
    ]
  },
  {
    "tag": "adapalene-acne",
    "name": "Adapalene Acne Treatment",
    "image_url": "https://mycorefix.com/cdn/shop/files/806ab02dfc5943d89fee5032b3392c3e_600x600.jpg",
    "product_url": "",
    "blurb": "Dermatologist-recommended retinoid gel for treating breakouts and improving skin texture.",
    "variant_id": "43290412187708",
    "price": "16.99",
    "benefits": [
      "Fights breakouts fast",
      "Improves skin clarity",
      "Recommended by dermatologists"
    ]
  },
  {
    "tag": "glossing-hair",
    "name": "Glossing Hair Lamination Mask",
    "image_url": "https://mycorefix.com/cdn/shop/files/f09ecbd717bc1165a207b9f5989adefc_600x600.jpg",
    "product_url": "",
    "blurb": "Hydrating mask to add instant shine, smooth frizz, and revive dull, dry hair.",
    "variant_id": "43318929817660",
    "price": "11.99",
    "benefits": [
      "Boosts shine instantly",
      "Tames frizz and flyaways",
      "Deeply hydrates dry hair"
    ]
  },
  {
    "tag": "dream-coat",
    "name": "Dream Coat Frizz Spray",
    "image_url": "https://mycorefix.com/cdn/shop/files/06f9b9a3f24025e338f91b38248b6c55_600x600.jpg",
    "product_url": "",
    "blurb": "Award-winning anti-humidity spray for sleek, shiny, frizz-free hair in any weather.",
    "variant_id": "43290366181436",
    "price": "32.99",
    "benefits": [
      "Controls frizz in any weather",
      "Adds sleek, shiny finish",
      "Award-winning humidity protection"
    ]
  },
  {
    "tag": "snail-nut",
    "name": "Snail Mucin Repair Serum",
    "image_url": "https://mycorefix.com/cdn/shop/files/8a352c2853c69aac8881c532b68ec02b_600x600.jpg",
    "product_url": "",
    "blurb": "K-beauty serum with snail mucin for deep hydration, skin repair, and a plump glow.",
    "variant_id": "43290362052668",
    "price": "19.99",
    "benefits": [
      "Deeply hydrates skin",
      "Promotes skin repair",
      "Boosts natural glow"
    ]
  },
  {
    "tag": "purifying-gel",
    "name": "Purifying Gel Cleanser",
    "image_url": "https://mycorefix.com/cdn/shop/files/38bd8e60ab7755be5ab4e25d2ee90b29_600x600.jpg",
    "product_url": "",
    "blurb": "Gentle foaming cleanser with niacinamide for effective, non-stripping face washing.",
    "variant_id": "43290361921596",
    "price": "19.99",
    "benefits": [
      "Effectively removes dirt and oil",
      "Non-stripping formula",
      "Infused with niacinamide"
    ]
  },
  {
    "tag": "repair-moisturizer",
    "name": "Barrier Repair Moisturizer",
    "image_url": "https://mycorefix.com/cdn/shop/files/2071075ddfe6b74dc1f32d41bf9ba51a_600x600.jpg",
    "product_url": "",
    "blurb": "Replenishing face cream with ceramides and niacinamide for all-day hydration and comfort.",
    "variant_id": "43290360643644",
    "price": "25.99",
    "benefits": [
      "Strengthens skin barrier",
      "Long-lasting hydration",
      "Comforts sensitive skin"
    ]
  },
  {
    "tag": "jelly-hydration",
    "name": "Collagen Jelly Hydration Cream",
    "image_url": "https://mycorefix.com/cdn/shop/files/b14117f26f53103f06a7901af700f8b9_600x600.jpg",
    "product_url": "",
    "blurb": "Lightweight, jelly-texture cream to boost skin hydration and restore a healthy glow.",
    "variant_id": "43290259488828",
    "price": "17.99",
    "benefits": [
      "Boosts moisture instantly",
      "Lightweight, non-greasy feel",
      "Restores healthy skin glow"
    ]
  },
  {
    "tag": "collagen-mask",
    "name": "Overnight Collagen Mask",
    "image_url": "https://mycorefix.com/cdn/shop/files/d8585845270221edcb9dc250da488b95_600x600.jpg",
    "product_url": "",
    "blurb": "Peel-off facial mask for elasticity, hydration, and visible overnight skin renewal.",
    "variant_id": "43290259390524",
    "price": "15.99",
    "benefits": [
      "Renews skin while you sleep",
      "Boosts elasticity and hydration",
      "Easy peel-off application"
    ]
  },
  {
    "tag": "deep-mask",
    "name": "Deep Hydration Collagen Mask",
    "image_url": "https://mycorefix.com/cdn/shop/files/2d395403325b8767b773118f6964beef_600x600.png",
    "product_url": "",
    "blurb": "Hydrogel mask for intense moisture, plumper skin, and minimized pores while you sleep.",
    "variant_id": "43290259357756",
    "price": "22.99",
    "benefits": [
      "Provides intense skin hydration",
      "Visibly plumps and smooths",
      "Reduces appearance of pores"
    ]
  },
  {
    "tag": "acne-patch",
    "name": "Hero Original Acne Patch",
    "image_url": "https://mycorefix.com/cdn/shop/files/fa523044a983520a27cc6ea3718228b4_600x600.png",
    "product_url": "",
    "blurb": "Best-selling hydrocolloid patches to visibly shrink pimples and protect healing skin.",
    "variant_id": "43290259226684",
    "price": "15.99",
    "benefits": [
      "Shrinks pimples overnight",
      "Protects healing blemishes",
      "Discreet and easy to use"
    ]
  },
  {
    "tag": "sleeptabs-night",
    "name": "Sleeptabs Night Sleep Aid",
    "image_url": "https://mycorefix.com/cdn/shop/files/5cba4ea51a4791e871eb845b056c071a_600x600.jpg",
    "product_url": "",
    "blurb": "Gentle, non-habit-forming sleep tablets to help you fall asleep and stay rested.",
    "variant_id": "43318934863932",
    "price": "16.99",
    "benefits": [
      "Promotes restful sleep",
      "Non-habit forming formula",
      "Helps you wake up refreshed"
    ]
  },
  {
    "tag": "melatonin-magnesium",
    "name": "Melatonin + Magnesium Sleep",
    "image_url": "https://mycorefix.com/cdn/shop/files/0b6b6f4c60aa2d914a7b874cd52feafb_600x600.jpg",
    "product_url": "",
    "blurb": "Melatonin and magnesium capsules to promote deep, restorative, natural sleep.",
    "variant_id": "43318933323836",
    "price": "34.99",
    "benefits": [
      "Supports deep, natural sleep",
      "Combines melatonin and magnesium",
      "Restores healthy sleep cycle"
    ]
  },
  {
    "tag": "apple-cider",
    "name": "Apple Cider Energy Gummies",
    "image_url": "https://mycorefix.com/cdn/shop/files/752333833c52fd737b9a13a8252741d0_600x600.jpg",
    "product_url": "",
    "blurb": "Delicious, vegan apple cider vinegar gummies with B12 to support metabolism and energy.",
    "variant_id": "43290240679996",
    "price": "17.99",
    "benefits": [
      "Supports energy naturally",
      "With apple cider & B12",
      "Vegan and delicious"
    ]
  },
  {
    "tag": "alpha-brain",
    "name": "Alpha Brain Focus Capsules",
    "image_url": "https://mycorefix.com/cdn/shop/files/fa6548bca8c482bcf0f58fbbf8d107ee_600x600.jpg",
    "product_url": "",
    "blurb": "Clinically tested nootropic to boost focus, mental clarity, and cognitive speed.",
    "variant_id": "43290213253180",
    "price": "29.99",
    "benefits": [
      "Improves focus and clarity",
      "Clinically tested nootropic",
      "Supports faster thinking"
    ]
  },
  {
    "tag": "nasal-strips",
    "name": "Extra Strength Nasal Strips",
    "image_url": "https://mycorefix.com/cdn/shop/files/fb08d00b8868517c9fc28fd9a69819a2_600x600.jpg",
    "product_url": "",
    "blurb": "Nasal strips to instantly relieve congestion and improve nighttime breathing.",
    "variant_id": "43290207453244",
    "price": "19.99",
    "benefits": [
      "Opens nasal passages",
      "Relieves congestion quickly",
      "Improves sleep quality"
    ]
  },
  {
    "tag": "pure-ash",
    "name": "Pure Organic Ashwagandha",
    "image_url": "https://mycorefix.com/cdn/shop/files/748e3f0d97f36c0aa1615a87a10a109c_600x600.jpg",
    "product_url": "",
    "blurb": "Premium adaptogen capsules for daily stress support and mood balance.",
    "variant_id": "43318930374716",
    "price": "19.99",
    "benefits": [
      "Balances mood and stress",
      "Organic adaptogen formula",
      "Supports daily wellbeing"
    ]
  },
  {
    "tag": "ash-d",
    "name": "Ashwagandha Vitamin D Gummies",
    "image_url": "https://mycorefix.com/cdn/shop/files/c3efcc9daaddc0de2d34901d72a85339_600x600.jpg",
    "product_url": "",
    "blurb": "Tasty berry gummies with KSM-66 ashwagandha and vitamin D for mood and relaxation.",
    "variant_id": "43290179469372",
    "price": "15.99",
    "benefits": [
      "Reduces stress & anxiety",
      "Supports immune health",
      "Delicious berry flavor"
    ]
  },
  {
    "tag": "bio-skin",
    "name": "Biotin Hair + Skin + Nails",
    "image_url": "https://mycorefix.com/cdn/shop/files/f0cd4d11997bfca94712c9de164934ab_600x600.jpg",
    "product_url": "",
    "blurb": "High-potency biotin softgels to support healthy hair, strong nails, and glowing skin.",
    "variant_id": "43290169311292",
    "price": "9.99",
    "benefits": [
      "Supports hair and nail growth",
      "Promotes glowing skin",
      "High potency biotin formula"
    ]
  },
  {
    "tag": "liquid-biotin",
    "name": "Liquid Multivitamin + Biotin",
    "image_url": "https://mycorefix.com/cdn/shop/files/790dbc83574dbbd94220b6d40c092168_600x600.jpg",
    "product_url": "",
    "blurb": "Advanced liquid formula for thicker hair, radiant skin, and overall wellness.",
    "variant_id": "43290161774652",
    "price": "46.99",
    "benefits": [
      "Thickens hair naturally",
      "Supports radiant skin",
      "Easy-absorb liquid formula"
    ]
  },
  {
    "tag": "keratin-boost",
    "name": "Biotin Collagen Keratin Boost",
    "image_url": "https://mycorefix.com/cdn/shop/files/86775a4746581d43e657c11236445b44_600x600.jpg",
    "product_url": "",
    "blurb": "Triple-action supplement for hair growth, skin elasticity, and nail strength.",
    "variant_id": "43290160988220",
    "price": "34.99",
    "benefits": [
      "Boosts hair, skin & nails",
      "Triple-action ingredients",
      "Promotes elasticity and strength"
    ]
  },
  {
    "tag": "pink-tape",
    "name": "Pink Premium Strip Tape",
    "image_url": "https://mycorefix.com/cdn/shop/files/0ae9cf9ee74dd8a718e16bf0b36731e5_600x600.jpg",
    "product_url": "",
    "blurb": "Strong, gentle adhesive strips for pain-free removal and multi-purpose use.",
    "variant_id": "43290148372540",
    "price": "17.99",
    "benefits": [
      "Pain-free removal",
      "Strong, secure hold",
      "Multipurpose use"
    ]
  },
  {
    "tag": "micropore-tape",
    "name": "Gentle Micropore Tape",
    "image_url": "https://mycorefix.com/cdn/shop/files/a31afc5376ca74145d6f3bdc94f1b405_600x600.jpg",
    "product_url": "",
    "blurb": "Soft, breathable medical tape for sensitive skin and secure everyday applications.",
    "variant_id": "43318925393980",
    "price": "5.99",
    "benefits": [
      "Soft and breathable",
      "Safe for sensitive skin",
      "Ideal for medical or home use"
    ]
  },
  {
    "tag": "coco-nut",
    "name": "Coconut Exfoliating Body Wash",
    "image_url": "https://mycorefix.com/cdn/shop/files/5f265d741784c3e05dab0efae43d5c7a_600x600.jpg",
    "product_url": "",
    "blurb": "Creamy, coconut-scented body wash with gentle exfoliants for smooth, glowing skin.",
    "variant_id": "43318925000764",
    "price": "7.99",
    "benefits": [
      "Gently exfoliates skin",
      "Nourishing coconut scent",
      "Leaves skin soft and smooth"
    ]
  },
  {
    "tag": "foaming-body",
    "name": "Foaming Face & Body Bar",
    "image_url": "https://mycorefix.com/cdn/shop/files/8b87f7cd8c2aa1339d31fc124cd6e96c_600x600.jpg",
    "product_url": "",
    "blurb": "Soap-free, fragrance-free cleansing bar for face and body—gentle enough for daily use.",
    "variant_id": "43264216399932",
    "price": "7.99",
    "benefits": [
      "Soap-free and gentle",
      "Fragrance-free formula",
      "Safe for face and body"
    ]
  },
  {
    "tag": "prebiotic-lotion",
    "name": "Daily Prebiotic Body Lotion",
    "image_url": "https://mycorefix.com/cdn/shop/files/dd32f3e7fecaaced1c51e376d8556ddf_600x600.jpg",
    "product_url": "",
    "blurb": "Non-greasy, 48-hour moisturizer with prebiotic oat for dry and sensitive skin.",
    "variant_id": "43264202768444",
    "price": "11.99",
    "benefits": [
      "48-hour long-lasting moisture",
      "Non-greasy, lightweight feel",
      "Prebiotic oat for sensitive skin"
    ]
  },
  {
    "tag": "white-machine",
    "name": "Portable White Noise Machine",
    "image_url": "https://mycorefix.com/cdn/shop/files/93525f64778147939d7ad0118129c417_600x600.jpg",
    "product_url": "",
    "blurb": "Travel-ready sound machine with soothing noise options for deep sleep and focus.",
    "variant_id": "43264197132348",
    "price": "29.99",
    "benefits": [
      "Promotes restful sleep anywhere",
      "Multiple soothing sound options",
      "Portable and travel-friendly"
    ]
  },
  {
    "tag": "plum-lip",
    "name": "Plum Perfect Lipstick",
    "image_url": "https://mycorefix.com/cdn/shop/files/38143d45ef6413fb73a702d433fbbd93_600x600.jpg",
    "product_url": "",
    "blurb": "Moisturizing, richly-pigmented lipstick in a universally flattering plum shade.",
    "variant_id": "43264188612668",
    "price": "13.99",
    "benefits": [
      "Rich, vibrant plum color",
      "Long-lasting hydration",
      "Universally flattering shade"
    ]
  },
  {
    "tag": "spot-gel",
    "name": "Benzoyl Spot Acne Gel",
    "image_url": "https://mycorefix.com/cdn/shop/files/3923285f63e427016a8927c53d0127ab_600x600.jpg",
    "product_url": "",
    "blurb": "Maximum strength benzoyl peroxide gel for rapid spot treatment of breakouts.",
    "variant_id": "43258045792316",
    "price": "7.99",
    "benefits": [
      "Targets breakouts fast",
      "Maximum strength formula",
      "Minimizes acne overnight"
    ]
  },
  {
    "tag": "daily-scrub",
    "name": "Gentle Daily Facial Scrub",
    "image_url": "https://mycorefix.com/cdn/shop/files/16113ff4b2d318ce881844761eebc8e7_600x600.jpg",
    "product_url": "",
    "blurb": "Oil-free daily face scrub to deep clean pores and smooth skin texture.",
    "variant_id": "43257719521340",
    "price": "8.99",
    "benefits": [
      "Deeply cleans pores",
      "Oil-free gentle formula",
      "Smooths and refines skin"
    ]
  },

  {
    "tag": "aloe-face",
    "name": "Aloe Rose Hydration Mist",
    "image_url": "https://mycorefix.com/cdn/shop/files/61gkFcU2s7L._SL1500.jpg",
    "product_url": "",
    "blurb": "Refreshing face spray with aloe, rosewater, and botanicals to hydrate and revive skin.",
    "variant_id": "43254188572732",
    "Price": "7.99",
    "benefits": [
            "Instantly hydrates skin",
            "Soothes redness and irritation",
            "Suitable for all skin types"
        ]
  }
];


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

