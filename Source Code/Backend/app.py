import json
import os
import re
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-prod")

# ============================
# CONFIG
# ============================
MIN_SCORE = 3.0  # Dataset currently has score=3; adjust here if your data changes

# ============================
# FILE PATHS
# ============================
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

MOVIE_SUMMARIES_FILE = os.path.join(DATA_DIR, "huggingface_movie_summaries.json")
GENRE_PREDICTIONS_FILE = os.path.join(DATA_DIR, "huggingface_genre_predictions.json")
TOPK_RECOMMENDATIONS_FILE = os.path.join(DATA_DIR, "huggingface_topk_recommendations.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# ensure users.json exists
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": []}, f, ensure_ascii=False, indent=2)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading {path}: {e}")
        return []


def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("users", [])
    except Exception:
        return []


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, ensure_ascii=False, indent=2)


# ============================
# LOAD DATASETS
# ============================
movie_summaries = load_json(MOVIE_SUMMARIES_FILE)
genre_predictions = load_json(GENRE_PREDICTIONS_FILE)
topk_recommendations = load_json(TOPK_RECOMMENDATIONS_FILE)


# ============================
# MERGE DATASETS
# ============================
movies_by_id = {}

for m in movie_summaries:
    movies_by_id[m.get("movie_id")] = {
        "movie_id": m.get("movie_id"),
        "title": m.get("title", ""),
        "summary": m.get("summary", "")
    }

for m in genre_predictions:
    mid = m.get("movie_id")
    if mid not in movies_by_id:
        movies_by_id[mid] = {
            "movie_id": mid,
            "title": m.get("title", ""),
            "summary": m.get("summary", "")
        }
    movies_by_id[mid]["predicted_genres"] = m.get("predicted_genres", [])

topk_by_id = {m.get("movie_id"): m for m in topk_recommendations}


# ============================
# SUMMARY CLEANING (2–3 lines)
# ============================
def clean_summary(text):
    """
    Cleans repetitive junk and trims to ~2–3 lines (~35 words).
    """
    if not text:
        return ""
    t = text.lower().strip()
    # remove repeated loops like "it's a ..."
    t = re.sub(r"(it's a [^,\.]+[,\.]?)+", " ", t)
    # dedupe words a bit (very light)
    words = t.split()
    cleaned = []
    seen = set()
    for w in words:
        if len(cleaned) > 200:
            break
        # keep some duplicates for naturalness if needed, but this simple pass
        # avoids the pathological repetitions in your dataset
        if w not in seen:
            cleaned.append(w)
            seen.add(w)
    t = " ".join(cleaned)
    # ~35 words -> 2–3 short lines visually
    MAX_WORDS = 35
    short = " ".join(t.split()[:MAX_WORDS])
    return (short.strip().capitalize() + "...") if short else ""


def safe_score(x):
    try:
        return float(x)
    except Exception:
        return 0.0


# ============================
# HOME (with navbar)
# ============================
@app.route("/")
def index():
    # build genres from predictions
    genre_set = set()
    for item in genre_predictions:
        for g in item.get("predicted_genres", []):
            if g and g.strip():
                genre_set.add(g.strip())
    genre_list = sorted(list(genre_set))
    username = session.get("username")
    return render_template("index.html", genres=genre_list, username=username)


# ============================
# RECOMMENDATION API (Top 10, score>=MIN_SCORE)
# ============================
@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.json or {}
    selected_genres = [g.lower().strip() for g in data.get("genres", []) if g and g.strip()]

    # Top rated first (from your top-k file) with safe score handling
    top_movies_pool = [m for m in topk_recommendations if safe_score(m.get("score")) >= MIN_SCORE]

    # Filter by selected genres if any
    if selected_genres:
        filtered = []
        for m in top_movies_pool:
            movie_genres = [g.lower() for g in m.get("predicted_genres", [])]
            if any(g in movie_genres for g in selected_genres):
                filtered.append(m)
        base = filtered
    else:
        base = top_movies_pool

    # Take top 10 and send cleaned copies
    movies = []
    for m in base[:10]:
        movies.append({
            "movie_id": m.get("movie_id"),
            "title": m.get("title"),
            "predicted_genres": m.get("predicted_genres", []),
            "score": safe_score(m.get("score")),
            "summary": clean_summary(m.get("summary", "")),
        })

    return jsonify(movies)


# ============================
# OPTIONAL APIs YOU ALREADY HAD
# ============================
@app.route("/api/movies")
def api_movies():
    # raw list (unchanged)
    return jsonify(list(movies_by_id.values()))


@app.route("/api/movie/<int:movie_id>")
def api_movie(movie_id):
    m = movies_by_id.get(movie_id)
    if not m:
        return abort(404)
    rec = topk_by_id.get(movie_id, {})
    detail = {
        "movie_id": m["movie_id"],
        "title": m["title"],
        "summary": clean_summary(m.get("summary", "")),
        "predicted_genres": m.get("predicted_genres", []),
        "score": safe_score(rec.get("score"))
    }
    return jsonify(detail)


# ============================
# AUTH & PAGES
# ============================
@app.route("/login", methods=["GET", "POST"])
def login():
    username = session.get("username")
    if request.method == "GET":
        return render_template("login.html", username=username)

    # POST
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()

    users = load_users()
    user = next((u for u in users if u.get("email") == email and u.get("password") == password), None)
    if user:
        session["username"] = user.get("name") or email
        return redirect(url_for("index"))
    else:
        return render_template("login.html", error="Invalid email or password.", username=username), 401


@app.route("/register", methods=["GET", "POST"])
def register():
    username = session.get("username")
    if request.method == "GET":
        return render_template("register.html", username=username)

    # POST
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()

    if not name or not email or not password:
        return render_template("register.html", error="All fields are required.", username=username), 400

    users = load_users()
    if any(u.get("email") == email for u in users):
        return render_template("register.html", error="Email already exists.", username=username), 409

    users.append({"name": name, "email": email, "password": password})
    save_users(users)

    session["username"] = name
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/about")
def about():
    username = session.get("username")

    team = [
        {
            "name": "Jagadeesh",
            "role": "Founder & Lead",
            "bio": "Drives product vision, DL integration, and platform scale.",
            "roll_number": "22471A0502",
            "image": "/static/team/22471A0502.jpg"
        },
        {
            "name": "Farooq",
            "role": "Frontend Engineer",
            "bio": "Builds delightful, accessible, fast UIs with Tailwind.",
            "roll_number": "22471A0551",
            "image": "/static/team/22471A0551.jpg"
        },
        {
            "name": "Noushik",
            "role": "Backend Engineer",
            "bio": "Scales APIs, optimizes data pipelines, and infra.",
            "roll_number": "22471A0552",
            "image": "/static/team/22471A0552.jpg"
        },
        {
            "name": "Balakrishna",
            "role": "Documentation Specialist",
            "bio": "Works on recommendations, evaluations, and metrics.",
            "roll_number": "22471A0542",
            "image": "/static/team/22471A0542.jpg"
        }
    ]

    return render_template("about.html", team=team, username=username)



@app.route("/contact", methods=["GET", "POST"])
def contact():
    username = session.get("username")
    message = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        body = request.form.get("message", "").strip()
        # For demo: just acknowledge; in real life, store/send email
        if name and email and subject and body:
            message = "Thanks! Your message has been received."
        else:
            message = "Please fill all fields."
    return render_template("contact.html", message=message, username=username)


# ============================
# RUN SERVER
# ============================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
