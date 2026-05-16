import os, random, json
from flask_mail import Message
from datetime import datetime
from pathlib import Path
import secrets
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from server.extensions import db, mail
from server.models.user import User
from server.models.post import ForumPost, ForumComment

app = Flask(__name__)
app.secret_key = "guildspace-dev-secret"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATA_DIR / 'forum.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""
app.config["MAIL_DEFAULT_SENDER"] = ""

app.config.from_pyfile("mail_config.py", silent=True)

db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "images", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Demo user until the real login/session system is connected.
# This makes the marketplace behave like a real app: users can only edit their own listings.
CURRENT_USER = "Sanchia"
CATEGORIES = ["Books", "Electronics", "Furniture", "Accommodation", "Accessories", "Food", "Other"]
STATUSES = ["Active", "Pending", "Sold"]

posts = [
    {
        "id": 1,
        "author": "uwastudentguild",
        "author_email": "",
        "title": "National Volunteer Week",
        "content": """Join us for an evening dedicated to recognising and thanking the incredible volunteers and partner organisations who give their time, energy, and passion to support our community 🙌""",
        "category": "Events",
        "image_url": "/static/images/forum/Volunteer.png",
        "created_at": datetime(2026, 5, 13, 18, 30),
        "likes": 14,
        "dislikes": 0,
        "comments": [
            {
                "author": "Maya",
                "text": "This sounds lovely! Are registrations required?",
                "created_at": datetime(2026, 5, 13, 19, 10)
            }
        ]
    },
    {
        "id": 2,
        "author": "Japanese Club at UWA",
        "author_email": "",
        "title": "Tokyo Alley",
        "content": """JSS is once again having a stall at @tokyoalleyperth this year 🎟️ Come down to Tokyo Alley and check out everything that’s being offered! JSS will be running the traditional Japanese game Fukuwarai as the activity, so try your hand at remaking the face blindfolded.""",
        "category": "Events",
        "image_url": "/static/images/forum/tokoyo.jpg",
        "created_at": datetime(2026, 5, 6, 13, 15),
        "likes": 21,
        "dislikes": 1,
        "comments": [
            {
                "author": "Aiko",
                "text": "The Fukuwarai activity sounds so fun!",
                "created_at": datetime(2026, 5, 6, 14, 5)
            }
        ]
    },
    {
        "id": 3,
        "author": "itsmsuofficial",
        "author_email": "",
        "title": "The Amber Lounge",
        "content": """Settle into the glow of a night filled with sound and soul…

MSU presents: The Amber Lounge, An all-ages charity concert featuring live performances all night, from local musicians and bands to dancers. Food and drinks available!""",
        "category": "Life",
        "image_url": "/static/images/forum/amber.png",
        "created_at": datetime(2026, 5, 1, 20, 0),
        "likes": 18,
        "dislikes": 0,
        "comments": []
    },
    {
        "id": 4,
        "author": "uwaartsunion",
        "author_email": "",
        "title": "Movie Night",
        "content": """Join us next Wednesday, 4-6PM, for AU x JSS’s movie night 🎥 Open to everyone, with free food included 🍕
No tickets required. Just drop by Austin Lecture Theatre alone or with your friends.""",
        "category": "Life",
        "image_url": "/static/images/forum/movie.png",
        "created_at": datetime(2026, 5, 11, 16, 0),
        "likes": 12,
        "dislikes": 0,
        "comments": [
            {
                "author": "Sam",
                "text": "Free food and anime movies is such a good combo.",
                "created_at": datetime(2026, 5, 11, 17, 20)
            }
        ]
    },
    {
        "id": 5,
        "author": "Sanchia",
        "author_email": "",
        "title": "Lost Stanley Mug",
        "content": """I lost my white Stanley tumbler with black polka dots in the food court area near the café/entrance today at noon.

It is very important to me. If anyone found it or handed it in to security, please comment or send me a message!""",
        "category": "LostFound",
        "image_url": "/static/images/forum/STANLEY.jpeg",
        "created_at": datetime(2026, 5, 14, 12, 10),
        "likes": 6,
        "dislikes": 0,
        "comments": [
            {
                "author": "Nidhi",
                "text": "I’ll keep an eye out near the café area.",
                "created_at": datetime(2026, 5, 14, 12, 45)
            }
        ]
    },
    {
        "id": 6,
        "author": "uwacareersemployability",
        "author_email": "",
        "title": "Work Integrated Learning Workshop",
        "content": """Thinking of applying for an internship for credit?Register for the Work Integrated Learning Workshop next week, Tuesday, to learn more about how you can source and apply for internships relevant to your study.""",
        "category": "Study",
        "image_url": "/static/images/forum/wil.png",
        "created_at": datetime(2026, 4, 5, 10, 30),
        "likes": 16,
        "dislikes": 0,
        "comments": []
    },
    {
        "id": 7,
        "author": "Abhishek",
        "author_email": "",
        "title": "Lost USB-C Charger",
        "content": """Hey everyone! I left my USB-C charger in Ross Lecture Theatre, possibly around row 3, earlier today.

If anyone has picked it up, please let me know. I'd really appreciate it!""",
        "category": "LostFound",
        "image_url": "/static/images/forum/charger.jpg",
        "created_at": datetime(2026, 5, 10, 15, 40),
        "likes": 5,
        "dislikes": 0,
        "comments": [
            {
                "author": "Priya",
                "text": "Maybe check with the lecture theatre lost property desk too.",
                "created_at": datetime(2026, 5, 10, 16, 5)
            }
        ]
    },
    {
        "id": 8,
        "author": "universityengineersclub",
        "author_email": "",
        "title": "Study Night",
        "content": """IG FINAL EXAM STUDY NIGHT!!!!Massive collab study night across multiple EMS units with tutors from different clubs all in one place.""",
        "category": "Study",
        "image_url": "/static/images/forum/exam.png",
        "created_at": datetime(2026, 5, 12, 18, 0),
        "likes": 28,
        "dislikes": 1,
        "comments": [
            {
                "author": "Daniel",
                "text": "This is exactly what I need before finals.",
                "created_at": datetime(2026, 5, 12, 18, 50)
            },
            {
                "author": "Sophie",
                "text": "Will CITS units be supported?",
                "created_at": datetime(2026, 5, 12, 19, 15)
            }
        ]
    },
    {
        "id": 9,
        "author": "perthinternational",
        "author_email": "",
        "title": "Boat Party",
        "content": """With the end of semester fast approaching, it’s time for our hottest event — RAVE ON THE WAVES 🌊🔥 The ultimate send-off is here. Our iconic semester boat party is back 🕺💃✨""",
        "category": "Life",
        "image_url": "/static/images/forum/rave.png",
        "created_at": datetime(2026, 5, 3, 19, 30),
        "likes": 25,
        "dislikes": 2,
        "comments": []
    },
    {
        "id": 10,
        "author": "venture_uwa",
        "author_email": "",
        "title": "Panel Night",
        "content": """What does the future of energy look like — and who is shaping it?On Tuesday, 22 April, we're bringing together leaders across industry, research, and startups to unpack the technologies, risks, and opportunities driving the global energy transition.""",
        "category": "Events",
        "image_url": "/static/images/forum/panel.jpg",
        "created_at": datetime(2026, 4, 16, 17, 45),
        "likes": 11,
        "dislikes": 0,
        "comments": []
    },
    {
        "id": 11,
        "author": "uwaguild_wellbeing",
        "author_email": "",
        "title": "Picnic Blankets, Poetry and Harmony",
        "content": """Picnic blankets, poetry, and harmony. Join us as we kick off Harmony Week with poems, food and good vibes! Bring a picnic blanket, invite your friends and enjoy a relaxed community event on campus.""",
        "category": "Events",
        "image_url": "/static/images/forum/picinic.png",
        "created_at": datetime(2026, 3, 11, 12, 0),
        "likes": 10,
        "dislikes": 0,
        "comments": []
    }
]

def seed_forum_demo_posts():
    """Seed demo forum posts into SQLite once if the forum table is empty."""
    if ForumPost.query.first():
        return

    for demo_post in posts:
        post = ForumPost(
            author=demo_post.get("author", "Anonymous"),
            author_email=demo_post.get("author_email", ""),
            title=demo_post.get("title", ""),
            content=demo_post.get("content", ""),
            category=demo_post.get("category", "Study"),
            image_url=demo_post.get("image_url", ""),
            likes=demo_post.get("likes", 0),
            dislikes=demo_post.get("dislikes", 0),
        )

        if hasattr(post, "created_at"):
            post.created_at = demo_post.get("created_at") or datetime.utcnow()

        db.session.add(post)
        db.session.flush()

        for demo_comment in demo_post.get("comments", []):
            comment = ForumComment(
                post_id=post.id,
                author=demo_comment.get("author", "You"),
                text=demo_comment.get("text", ""),
            )

            if hasattr(comment, "created_at"):
                comment.created_at = demo_comment.get("created_at") or datetime.utcnow()

            db.session.add(comment)

    db.session.commit()


with app.app_context():
    seed_forum_demo_posts()

items = [
    {
        "id": 1,
        "title": "MacBook Air",
        "price": 450,
        "image": "macbookair.jpeg",
        "seller": "Sanchia",
        "time": "1d ago",
        "category": "Electronics",
        "status": "Pending",
        "description": "Good condition laptop, perfect for assignments and coding."
    },
    {
        "id": 2,
        "title": "Shared Room Available",
        "price": 180,
        "image": "room.jpeg",
        "seller": "Noah",
        "time": "6h ago",
        "category": "Accommodation",
        "status": "Active",
        "description": "Room available near UWA. Includes Wi-Fi and furnished space."
    },
    {
        "id": 3,
        "title": "Headphones",
        "price": 60,
        "image": "headphones.jpeg",
        "seller": "Sophia",
        "time": "1d ago",
        "category": "Electronics",
        "status": "Sold",
        "description": "Noise-cancelling headphones, good for library and travel."
    },
    {
        "id": 4,
        "title": "AirPods",
        "price": 15,
        "image": "airpods.jpeg",
        "seller": "Mia",
        "time": "2h ago",
        "category": "Other",
        "status": "Pending",
        "description": "Protective AirPods case with keychain attachment."
    },
    {
        "id": 5,
        "title": "Homemade Brownies",
        "price": 8,
        "image": "brownies.jpeg",
        "seller": "Ava",
        "time": "Just now",
        "category": "Food",
        "status": "Active",
        "description": "Fresh brownies available for pickup near campus."
    },
    {
        "id": 6,
        "title": "Book",
        "price": 20,
        "image": "book.jpg",
        "seller": "Nidhi",
        "time": "3d ago",
        "category": "Books",
        "status": "Sold",
        "description": "good book to read"
    },
    {
        "id": 7,
        "title": "Chair",
        "price": 15,
        "image": "chair.jpg",
        "seller": "Esther",
        "time": "5h ago",
        "category": "Furniture",
        "status": "Pending",
        "description": "can be paired with a study table"
    },
    {
        "id": 8,
        "title": "Coach Bag",
        "price": 500,
        "image": "bag.jpg",
        "seller": "Zeyu",
        "time": "Just now",
        "category": "Accessories",
        "status": "Active",
        "description": "Almost new"
    }
]

messages = []
bids = [
    {
        "id": 1,
        "item_id": 1,
        "item_title": "MacBook Air",
        "seller": "Sanchia",
        "buyer_name": "Maya",
        "buyer_email": "maya@student.uwa.edu.au",
        "bid_amount": "420",
        "time": "29 Apr, 07:30 PM"
    }
]
MARKETPLACE_DATA_FILE = DATA_DIR / "marketplace.json"


def load_marketplace_data():
    """Load marketplace listings, messages and bids from JSON if available."""
    global items, messages, bids

    if not MARKETPLACE_DATA_FILE.exists():
        save_marketplace_data()
        return

    try:
        with open(MARKETPLACE_DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        items = data.get("items", items)
        messages = data.get("messages", messages)
        bids = data.get("bids", bids)

    except (OSError, json.JSONDecodeError):
        # If the JSON file is missing/corrupt, keep the default demo data.
        save_marketplace_data()


def save_marketplace_data():
    """Save marketplace listings, messages and bids to JSON."""
    data = {
        "items": items,
        "messages": messages,
        "bids": bids,
    }

    with open(MARKETPLACE_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

load_marketplace_data()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_item(item_id):
    return next((item for item in items if item["id"] == item_id), None)

def get_forum_post(post_id):
    return next((post for post in posts if post["id"] == post_id), None)


def logged_in():
    return "user_id" in session


def current_user_name():
    return session.get("user_name", CURRENT_USER)


def current_user_first_name():
    name = session.get("user_name", "")
    return name.split()[0] if name else CURRENT_USER


def current_user_email():
    return session.get("user_email", "")


def is_owner(item):
    return item and item.get("seller") == current_user_first_name()

def create_otp():
    return str(random.randint(100000,999999))

def send_otp(email, otp):
    print(f"OTP for {email}: {otp}")
    return True

def create_csrf_token():
    """Create one CSRF token per browser session and reuse it in all forms."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]

@app.context_processor
def inject_common_data():
    current_user = current_user_first_name()

    unread_count = len([
        message for message in messages
        if message.get("seller") == current_user and not message.get("read")
    ])

    own_bid_count = len([
        bid for bid in bids
        if bid.get("seller") == current_user
    ])

    return {
        "logged_in": "user_id" in session,
        "logged_in_user": session.get("user_name"),
        "unread_count": unread_count,
        "own_bid_count": own_bid_count,
        "categories": CATEGORIES,
        "statuses": STATUSES,
        "current_user": current_user,
        "csrf_token": create_csrf_token,
    }

@app.before_request
def check_csrf_token():
    """Block POST requests that do not include the correct CSRF token."""
    if request.method == "POST":
        form_token = request.form.get("csrf_token")
        session_token = session.get("csrf_token")

        if not form_token or not session_token or form_token != session_token:
            abort(403)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/forum")
def forum():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    forum_posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()

    return render_template(
        "forum.html",
        posts=forum_posts,
        active_nav="forum"
    )

@app.route("/forum/post", methods=["POST"])
def create_post():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    author = request.form.get("author", "").strip() or session.get("user_name", "Anonymous")
    author_email = request.form.get("author_email", "").strip()
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    category = request.form.get("category", "Study").strip()

    if not title or not content or not category:
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for("forum"))

    image_url = ""
    image_file = request.files.get("image_file")

    if image_file and image_file.filename:
        if not allowed_file(image_file.filename):
            flash("Please upload a valid image file: png, jpg, jpeg, gif, or webp.", "danger")
            return redirect(url_for("forum"))

        safe_name = secure_filename(image_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{safe_name}"

        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image_file.save(image_path)

        image_url = url_for("static", filename=f"images/uploads/{filename}")

    new_post = ForumPost(
        author=author,
        author_email=author_email,
        title=title,
        content=content,
        category=category,
        image_url=image_url,
        likes=0,
        dislikes=0,
    )

    if hasattr(new_post, "user_id"):
        new_post.user_id = session.get("user_id")

    db.session.add(new_post)
    db.session.commit()

    flash("Post published successfully.", "success")
    return redirect(url_for("forum", _anchor=f"post-{new_post.id}"))


@app.route("/forum/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    post = ForumPost.query.get_or_404(post_id)
    post.likes = int(post.likes or 0) + 1
    db.session.commit()

    return redirect(url_for("forum", _anchor=f"post-{post_id}"))

@app.context_processor
def inject_forum_helpers():
    def category_label(category):
        return "Lost & Found" if category == "LostFound" else category

    def relative_time(value):
        if not value:
            return ""

        now = datetime.utcnow()
        diff = now - value

        if diff.days == 0:
            if diff.seconds < 60:
                return "just now"
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} min ago"
            hours = diff.seconds // 3600
            return f"{hours} hr ago"

        if diff.days == 1:
            return "yesterday"

        return value.strftime("%d %b %Y")

    return {
        "category_label": category_label,
        "relative_time": relative_time
    }


@app.route("/forum/<int:post_id>/dislike", methods=["POST"])
def dislike_post(post_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    post = ForumPost.query.get_or_404(post_id)
    post.dislikes = int(post.dislikes or 0) + 1
    db.session.commit()

    return redirect(url_for("forum", _anchor=f"post-{post_id}"))


@app.route("/forum/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    post = ForumPost.query.get_or_404(post_id)
    text = request.form.get("text", "").strip()

    if not text:
        flash("Comment cannot be empty.", "danger")
        return redirect(url_for("forum", _anchor=f"post-{post_id}"))

    comment = ForumComment(
        post_id=post.id,
        text=text,
        author=session.get("user_name", "You"),
    )

    if hasattr(comment, "user_id"):
        comment.user_id = session.get("user_id")

    db.session.add(comment)
    db.session.commit()

    flash("Comment added.", "success")
    return redirect(url_for("forum", _anchor=f"post-{post_id}"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        
        if not user.is_verified:
            flash("Account not verified, please verify before logging in.")
            return redirect(url_for("otp_verification", email=user.email))
        
        # This will keep the login session until we logout
        session["user_id"] = user.id
        session["user_name"] = user.full_name
        session["user_email"] = user.email

        
        return redirect(url_for("home"))
    return render_template("login.html", active_nav="login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("firstName", "").strip()
        last_name = request.form.get("lastName", "").strip()
        email = request.form.get("email", "").strip().lower()
        dob = request.form.get("dob", "").strip()
        gender = request.form.get("gender", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm-password", "")

        if not first_name or not last_name or not email or not dob or not gender or not password:
            flash("Please fill all required fields.")
            return redirect(url_for("register"))

        if not email.endswith("@student.uwa.edu.au"):
            flash("Please use your UWA student email.")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.is_verified:
            flash("This email is already registered. Please login.")
            return redirect(url_for("login"))
        
        if existing_user and not existing_user.is_verified:
            otp = create_otp()

            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.dob = dob
            existing_user.gender = gender
            existing_user.otp_number = otp
            existing_user.otp_generation_time = datetime.now()
            existing_user.set_password(password)

            db.session.commit()

            send_otp(email, otp)

            flash("Account already registered but not verified. A new OTP has been sent to your email, please verify!")
            return redirect(url_for("otp_verification", email=email))


        otp = create_otp()

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            dob=dob,
            gender=gender,
            is_verified=False,
            otp_number=otp,
            otp_generation_time=datetime.now(),
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        send_otp(email, otp)

        flash("Account created successfully. Please check your email for OTP.")
        return redirect(url_for("otp_verification", email=email))

    return render_template("register.html", active_nav="register")

@app.route("/verify-otp", methods=["GET", "POST"])
def otp_verification():
    email = request.args.get("email", "").strip().lower()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        entered_otp = request.form.get("otp", "").strip()

        user = User.query.filter_by(email=email).first()

        if not user or user.otp_number != entered_otp:
            flash("Invalid OTP. Please try again.")
            return redirect(url_for("otp_verification", email=email))

        user.is_verified = True
        user.otp_number = None
        user.otp_generation_time = None

        db.session.commit()

        flash("Email verified successfully. You can now login.")
        return redirect(url_for("login"))

    return render_template("otp_verification.html", email=email)


@app.route("/marketplace")
def marketplace():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    selected_category = request.args.get("category", "All")
    search_query = request.args.get("q", "").strip().lower()

    filtered_items = items

    if selected_category != "All":
        filtered_items = [item for item in filtered_items if item["category"] == selected_category]

    if search_query:
        filtered_items = [
            item for item in filtered_items
            if search_query in item["title"].lower()
            or search_query in item["seller"].lower()
            or search_query in item["category"].lower()
            or search_query in item["description"].lower()
        ]

    return render_template(
        "marketplace.html",
        items=filtered_items,
        selected_category=selected_category,
        search_query=request.args.get("q", "")
    )


@app.route("/post-listing", methods=["GET", "POST"])
def post_listing():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    if request.method == "POST":
        image_file = request.files.get("image")
        image_name = "placeholder-other.svg"

        if image_file and image_file.filename:
            if allowed_file(image_file.filename):
                safe_name = secure_filename(image_file.filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_name = f"uploads/{timestamp}_{safe_name}"
                image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{timestamp}_{safe_name}"))
            else:
                flash("Please upload a valid image file: png, jpg, jpeg, gif, or webp.")
                return redirect(url_for("post_listing"))

        category = request.form["category"]
        if category not in CATEGORIES:
            flash("Please choose a valid category.")
            return redirect(url_for("post_listing"))

        new_item = {
            "id": max(item["id"] for item in items) + 1 if items else 1,
            "title": request.form["title"],
            "price": int(request.form["price"]),
            "image": image_name,
            "seller": current_user_first_name(),
            "time": "Just now",
            "category": category,
            "status": "Active",
            "description": request.form["description"]
        }
        items.insert(0, new_item)
        save_marketplace_data()
        flash("Listing posted successfully.")
        return redirect(url_for("marketplace"))

    return render_template("post_listing.html")


@app.route("/message-seller/<int:item_id>", methods=["GET", "POST"])
def message_seller(item_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    selected_item = get_item(item_id)

    if not selected_item:
        flash("Listing not found.")
        return redirect(url_for("marketplace"))

    if is_owner(selected_item):
        flash("You cannot message yourself for your own listing.")
        return redirect(url_for("marketplace"))

    if selected_item["status"] == "Sold":
        flash("This listing is sold, so messages are closed.")
        return redirect(url_for("marketplace"))

    if request.method == "POST":
        messages.insert(0, {
            "id": len(messages) + 1,
            "item_id": selected_item["id"],
            "item_title": selected_item["title"],
            "seller": selected_item["seller"],
            "buyer_name": request.form.get("name", "").strip() or current_user_name(),
            "buyer_email": request.form.get("email", "").strip() or current_user_email(),
            "message": request.form["message"],
            "time": datetime.now().strftime("%d %b, %I:%M %p"),
            "read": False
        })
        save_marketplace_data()
        flash("Message sent successfully.")
        return redirect(url_for("marketplace"))

    return render_template("message_seller.html", item=selected_item)


@app.route("/bid/<int:item_id>", methods=["POST"])
def place_bid(item_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    selected_item = get_item(item_id)

    if not selected_item:
        flash("Listing not found.")
        return redirect(url_for("marketplace"))

    if is_owner(selected_item):
        flash("You cannot place a bid on your own listing.")
        return redirect(url_for("marketplace"))

    if selected_item["status"] != "Pending":
        flash("Bids are only open when a listing is Pending.")
        return redirect(url_for("marketplace"))

    bids.insert(0, {
        "id": len(bids) + 1,
        "item_id": selected_item["id"],
        "item_title": selected_item["title"],
        "seller": selected_item["seller"],
        "buyer_name": request.form.get("buyer_name", "").strip() or current_user_name(),
        "buyer_email": request.form.get("buyer_email", "").strip() or current_user_email(),
        "bid_amount": request.form["bid_amount"],
        "time": datetime.now().strftime("%d %b, %I:%M %p")
    })
    save_marketplace_data()
    flash("Bid placed successfully.")
    return redirect(url_for("marketplace"))


@app.route("/listing/<int:item_id>/status", methods=["POST"])
def update_listing_status(item_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    selected_item = get_item(item_id)

    if not selected_item:
        flash("Listing not found.")
        return redirect(url_for("marketplace"))

    if not is_owner(selected_item):
        flash("You can only update your own listings.")
        return redirect(url_for("marketplace"))

    new_status = request.form.get("status")
    if new_status not in STATUSES:
        flash("Invalid listing status.")
        return redirect(url_for("marketplace"))

    selected_item["status"] = new_status
    save_marketplace_data()
    flash(selected_item["title"] + " status changed to " + new_status + ".")
    return redirect(request.referrer or url_for("marketplace"))


@app.route("/messages")
def view_messages():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    own_messages = [
    message for message in messages
    if message.get("seller") == current_user_first_name()
]
    for message in own_messages:
        message["read"] = True
    save_marketplace_data()
    return render_template("messages.html", messages=own_messages)


@app.route("/bids")
def view_bids():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    own_bids = [
    bid for bid in bids
    if bid.get("seller") == current_user_first_name()
]
    return render_template("bids.html", bids=own_bids)

@app.route("/logout")
def logout():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

