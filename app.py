import os, random
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


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_item(item_id):
    return next((item for item in items if item["id"] == item_id), None)


def is_owner(item):
    return item and item.get("seller") == CURRENT_USER

def logged_in():
    return "user_id" in session

def create_otp():
    return str(random.randint(100000,999999))

def send_otp(email, otp):
    if not app.config.get("MAIL_DEFAULT_SENDER") or not app.config.get("MAIL_USERNAME"):
        print(f"[DEV OTP] Email: {email}, OTP: {otp}")
        return False

    message = Message(
        subject="OTP for verification",
        recipients=[email],
        sender=app.config["MAIL_DEFAULT_SENDER"],
        body="Your one time password (OTP) to login to your GuildSpace account securely is: " + otp
    )

    return mail.send(message)

def create_csrf_token():
    """Create one CSRF token per browser session and reuse it in all forms."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]

@app.context_processor
def inject_common_data():
    unread_count = len([message for message in messages if message.get("seller") == CURRENT_USER and not message.get("read")])
    own_bid_count = len([bid for bid in bids if bid.get("seller") == CURRENT_USER])
    return {
        "logged_in": "user_id" in session,
        "logged_in_user": session.get("user_name"),
        "unread_count": unread_count,
        "own_bid_count": own_bid_count,
        "categories": CATEGORIES,
        "statuses": STATUSES,
        "current_user": CURRENT_USER,
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

    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()

    return render_template(
        "forum.html",
        posts=posts,
        active_nav="forum"
    )

@app.route("/forum/post", methods=["POST"])
def create_post():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    category = request.form.get("category", "Study").strip()
    author = request.form.get("author", "").strip() or session.get("user_name", "Anonymous")
    author_email = request.form.get("author_email", "").strip()

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
        title=title,
        content=content,
        category=category,
        author=author,
        author_email=author_email,
        image_url=image_url,
        user_id=session.get("user_id")
    )

    db.session.add(new_post)
    db.session.commit()

    flash("Post published successfully.", "success")
    return redirect(url_for("forum"))


@app.route("/forum/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    post = ForumPost.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()

    return redirect(url_for("forum"))

@app.context_processor
def inject_forum_helpers():
    def category_label(category):
        return "Lost & Found" if category == "LostFound" else category

    def relative_time(value):
        return "just now"

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
    post.dislikes += 1
    db.session.commit()

    return redirect(url_for("forum"))


@app.route("/forum/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))

    post = ForumPost.query.get_or_404(post_id)
    text = request.form.get("text", "").strip()

    if not text:
        flash("Comment cannot be empty.", "danger")
        return redirect(url_for("forum"))

    comment = ForumComment(
        post_id=post.id,
        text=text,
        author=session.get("user_name", "You"),
        user_id=session.get("user_id")
    )

    db.session.add(comment)
    db.session.commit()

    flash("Comment added.", "success")
    return redirect(url_for("forum"))


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
            "seller": CURRENT_USER,
            "time": "Just now",
            "category": category,
            "status": "Active",
            "description": request.form["description"]
        }
        items.insert(0, new_item)
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
            "buyer_name": request.form["name"],
            "buyer_email": request.form["email"],
            "message": request.form["message"],
            "time": datetime.now().strftime("%d %b, %I:%M %p"),
            "read": False
        })
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
        "buyer_name": request.form["buyer_name"],
        "buyer_email": request.form["buyer_email"],
        "bid_amount": request.form["bid_amount"],
        "time": datetime.now().strftime("%d %b, %I:%M %p")
    })
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
    flash(selected_item["title"] + " status changed to " + new_status + ".")
    return redirect(request.referrer or url_for("marketplace"))


@app.route("/messages")
def view_messages():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    own_messages = [message for message in messages if message.get("seller") == CURRENT_USER]
    for message in own_messages:
        message["read"] = True
    return render_template("messages.html", messages=own_messages)


@app.route("/bids")
def view_bids():
    if not logged_in():
        flash("Please login first.")
        return redirect(url_for("login"))
    own_bids = [bid for bid in bids if bid.get("seller") == CURRENT_USER]
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

