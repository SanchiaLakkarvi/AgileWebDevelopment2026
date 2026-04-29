import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "guildspace-dev-secret"

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


@app.context_processor
def inject_common_data():
    unread_count = len([message for message in messages if message.get("seller") == CURRENT_USER and not message.get("read")])
    own_bid_count = len([bid for bid in bids if bid.get("seller") == CURRENT_USER])
    return {
        "unread_count": unread_count,
        "own_bid_count": own_bid_count,
        "categories": CATEGORIES,
        "statuses": STATUSES,
        "current_user": CURRENT_USER,
    }


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/forum")
def forum():
    return render_template("forum.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/marketplace")
def marketplace():
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
    own_messages = [message for message in messages if message.get("seller") == CURRENT_USER]
    for message in own_messages:
        message["read"] = True
    return render_template("messages.html", messages=own_messages)


@app.route("/bids")
def view_bids():
    own_bids = [bid for bid in bids if bid.get("seller") == CURRENT_USER]
    return render_template("bids.html", bids=own_bids)


if __name__ == "__main__":
    app.run(debug=True)
