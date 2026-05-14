# GuildSpace – AgileWebDevelopment2026

GuildSpace is a student-focused web application developed for the **Agile Web Development 2026** group project. The application is designed as a simple campus community platform where students can access key pages such as the homepage, forum, marketplace, login, and registration pages.

The current version includes core page navigation, forum access, and a more developed **Marketplace** module with listing creation, image uploads, messaging, bidding, and seller-side controls.

---

## Project Description

This project demonstrates a Flask-based web application using server-side rendering with Jinja templates. It simulates a university community platform where students can interact through shared pages and marketplace features.

The application currently runs as a local development/demo version. It uses Flask for backend routing, Jinja for template rendering, HTML/CSS for the frontend interface, and simple demo data structures for marketplace functionality.

The project is intended to demonstrate key agile web development concepts such as:

- Flask routing
- Jinja template rendering
- Form handling
- Image uploads
- Static file management
- Marketplace listing creation
- Messaging and bidding workflows
- Basic seller ownership behaviour
- Manual testing and GitHub workflow

---

## Main Features

- Homepage with navigation to key sections of the site
- Login and registration page templates
- Forum page access
- Marketplace page with item cards
- Category filtering and search functionality
- Create listing form with image upload support
- Listing status system using `Active`, `Pending`, and `Sold`
- Seller-only status update behaviour for owned listings
- Message seller feature
- Inbox page for viewing messages received by the current seller
- Bidding feature for listings with `Pending` status
- Bids page for sellers to view bids placed on their own listings
- Shared base template and consistent styling through static CSS

> Note: This is a course/demo version. Some features such as real user authentication, persistent marketplace database storage, and production-level email notifications are not fully connected yet.

---

## Group Members

Replace the placeholder details below with the final group member names, student IDs, and contribution details before submission.

| Name | Student ID | Main Contribution / Responsibility |
|---|---:|---|
| Sanchia Recson Lakkarvi | 24732787 | Marketplace page, listing upload, bidding, messaging/inbox flow, seller-side controls, README update, documentation|
| Zeyu Wang| 23320288 | Homepage, Forum page, navigation, and UI support |
| Nikhil Chadha | 24231774 | Login and registration pages |

---

## Technology Stack

| Area | Technology Used |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Jinja templates |
| Styling | CSS, Bootstrap-style layout concepts |
| File Uploads | Werkzeug secure filename handling |
| Data Storage | In-memory Python lists for marketplace demo data |
| Database | SQLite for forum-related data |
| Assets | Static images and uploaded images |
| Version Control | Git and GitHub |

---

## Project Structure

```text
AgileWebDevelopment2026-main-3/
├── app.py
├── requirements.txt
├── mail_config.py
├── README.md
├── data/
│   └── forum.db
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── forum.html
│   ├── marketplace.html
│   ├── post_listing.html
│   ├── message_seller.html
│   ├── messages.html
│   └── bids.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│       ├── uploads/
│       └── marketplace image files
├── server/
│   ├── routes/
│   ├── models/
│   └── utils/
├── src/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── uploads/
├── planning/
└── design/