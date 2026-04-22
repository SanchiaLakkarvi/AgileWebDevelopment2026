from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Keep items global so new listings can be added
items = [
    {
        "id": 1,
        "title": "MacBook Air",
        "price": 450,
        "image": "laptop.jpg",
        "seller": "Liam",
        "time": "1d ago",
        "category": "Electronics",
        "description": "Good condition laptop, perfect for assignments and coding."
    },
    {
        "id": 2,
        "title": "Shared Room Available",
        "price": 180,
        "image": "room.jpg",
        "seller": "Noah",
        "time": "6h ago",
        "category": "Accommodation",
        "description": "Room available near UWA. Includes Wi-Fi and furnished space."
    },
    {
        "id": 3,
        "title": "Headphones",
        "price": 60,
        "image": "headphones.jpg",
        "seller": "Sophia",
        "time": "1d ago",
        "category": "Electronics",
        "description": "Noise-cancelling headphones, good for library and travel."
    },
    {
        "id": 4,
        "title": "Zodiac Book",
        "price": 20,
        "image": "book.jpg",
        "seller": "Ava",
        "time": "5h ago",
        "category": "Books",
        "description": "Useful first-year textbook with clean pages and notes."
    },
    {
        "id": 5,
        "title": "iPhone",
        "price": 250,
        "image": "phone.jpg",
        "seller": "Esther",
        "time": "3d ago",
        "category": "Electronics",
        "description": "Used phone in working condition. Slight wear but runs well."
    },
    {
        "id": 6,
        "title": "Study Chair",
        "price": 35,
        "image": "chair.jpg",
        "seller": "Benjamin",
        "time": "2d ago",
        "category": "Furniture",
        "description": "Comfortable chair for study setup. Pickup from campus."
    },
    {
        "id": 7,
        "title": "Coach Bag",
        "price": 30,
        "image": "bag.jpg",
        "seller": "Daniel",
        "time": "2d ago",
        "category": "Accessories",
        "description": "Spacious backpack, perfect for uni and daily use."
    },
    {
        "id": 8,
        "title": "Table Lamp",
        "price": 25,
        "image": "lamp.jpg",
        "seller": "Lucas",
        "time": "3h ago",
        "category": "Furniture",
        "description": "Minimal desk lamp, perfect for night study sessions."
    }
]


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
    return render_template("marketplace.html", items=items)


@app.route("/post-listing", methods=["GET", "POST"])
def post_listing():
    if request.method == "POST":
        new_item = {
            "id": len(items) + 1,
            "title": request.form["title"],
            "price": int(request.form["price"]),
            "image": request.form["image"],
            "seller": request.form["seller"],
            "time": "Just now",
            "category": request.form["category"],
            "description": request.form["description"]
        }
        items.append(new_item)
        return redirect(url_for("marketplace"))

    return render_template("post_listing.html")


@app.route("/message-seller/<int:item_id>")
def message_seller(item_id):
    selected_item = next((item for item in items if item["id"] == item_id), None)
    return render_template("message_seller.html", item=selected_item)


if __name__ == "__main__":
    app.run(debug=True)