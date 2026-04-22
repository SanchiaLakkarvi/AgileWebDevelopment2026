# AgileWebDevelopment2026

## Minimal Backend Setup (Flask + Jinja)

This project is simplified to match the lecture baseline:
- Flask server
- Jinja templates for server-side rendering
- Basic form handling with POST + redirect
- Forum data persisted in SQLite via SQLAlchemy
- Marketplace flow handled with in-memory listings

No AJAX API is required in this simplified version.

## Project Structure

- `app.py`: app entry point only
- `server/`: backend package
- `server/__init__.py`: app factory and configuration
- `server/forum/models.py`: forum database models
- `server/forum/routes.py`: forum routes and handlers
- `server/marketplace/routes.py`: marketplace routes and handlers
- `templates/base.html`: shared Jinja layout
- `templates/forum.html`: forum page (server-rendered posts + forms)
- `src/styles/`: CSS files
- `src/components/navbar.js`: reusable navbar component

## Run Locally

1. Create and activate a virtual environment
2. Install dependencies
3. Start server

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
pip install flask-sqlalchemy
python app.py
```

Open:
- `http://127.0.0.1:5000/` (home)
- `http://127.0.0.1:5000/forum`
- `http://127.0.0.1:5000/marketplace`

## Main Routes

- `GET /`
- `GET /forum`
- `GET /marketplace`
- `GET/POST /post-listing`
- `GET /message-seller/<item_id>`
- `POST /forum/post`
- `POST /forum/<post_id>/like`
- `POST /forum/<post_id>/dislike`
- `POST /forum/<post_id>/comment`
