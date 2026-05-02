# GuildSpace (AgileWebDevelopment2026)

A Flask + Jinja course project (local demo version).

## 1. Project Overview

This project currently follows a **client-server architecture**:
- Backend: Flask (routing, template rendering, form handling)
- Frontend: Jinja templates + Bootstrap + existing static CSS/JS
- Data: SQLite (Forum), in-memory list (Marketplace)
- Email: Flask-Mail (Forum comment notifications)

## 2. Current Folder Structure

```text
.
├── app.py
├── mail_config.py
├── data/
│   └── forum.db
├── server/
│   ├── __init__.py
│   ├── extensions.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── forum.py
│   │   └── marketplace.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── forum.py
│   └── utils/
│       ├── __init__.py
│       └── mailer.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── forum.html
│   ├── marketplace.html
│   ├── post_listing.html
│   └── message_seller.html
├── src/
│   ├── components/
│   │   └── navbar.js
│   ├── pages/
│   │   └── Forum/forum.js
│   ├── styles/
│   │   ├── global.css
│   │   ├── homepage.css
│   │   ├── login.css
│   │   ├── forum.css
│   │   └── marketplace.css
│   ├── uploads/
│   └── assets/
└── static/
    └── images/
```

## 3. Run Locally

### 3.1 Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-sqlalchemy flask-mail
```

### 3.2 Start the server

```bash
python3 app.py
```

Default URL: `http://127.0.0.1:5000`

## 4. Page Entry Points

- Home: `GET /`
- Login: `GET /login`
- Register: `GET /register`
- Forum: `GET /forum`
- Marketplace: `GET /marketplace`

## 5. Main Route Details

### 5.1 Forum (database-backed)

- `GET /forum`: render forum page
- `POST /forum/post`: create a post (supports image upload)
- `POST /forum/<post_id>/like`: like a post
- `POST /forum/<post_id>/dislike`: dislike a post
- `POST /forum/<post_id>/comment`: add a comment

Forum data is stored in SQLite: `data/forum.db`.

### 5.2 Marketplace (in-memory data)

- `GET /marketplace`: marketplace page
- `GET|POST /post-listing`: create a listing
- `GET /message-seller/<item_id>`: message seller
- `GET /market-images/<filename>`: serve marketplace images

Current Marketplace items are defined in `server/routes/marketplace.py` (`items` list) and reset on restart.

## 6. Static Assets and Templates

### 6.1 Flask static mapping

In `server/__init__.py`:
- `static_folder` points to `src`
- `static_url_path` is `/static`

So template static references use:
- `{{ url_for('static', filename='styles/forum.css') }}`
- `{{ url_for('static', filename='components/navbar.js') }}`

### 6.2 Image storage

- Forum user uploads: saved to `src/uploads/`, served as `/static/uploads/...`
- Marketplace images: stored in `static/images/`, served via `/market-images/...`

## 7. Email Notifications (Forum Comments)

When someone comments on a post, the app attempts to send an email to the post owner if an email address is provided.

Configuration file: `mail_config.py`

Config keys:
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_USE_SSL`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`

> Note: For this course demo, file-based config is allowed. In production, use environment variables.

## 8. Development Conventions

- `app.py` is startup entry only.
- Put Flask routes in `server/routes/`.
- Put database models in `server/models/`.
- Put shared logic (e.g., email) in `server/utils/`.
- Render pages from `templates/`; `src/pages/*` can be kept as static prototypes, not Flask render entry points.

## 9. FAQ

### 9.1 Why does the page not reflect DB changes?

Check:
- Server restarted
- You are operating on `data/forum.db`
- You are visiting Flask routes (not opening local HTML files directly)

### 9.2 Why is an uploaded image not visible?

Check:
- Form uses `enctype="multipart/form-data"`
- File is saved in `src/uploads/`
- Page references `/static/uploads/...`

---

For future extension (real login auth, register persistence, OTP, centralized config), continue building in `server/utils/` and `server/models/`.
