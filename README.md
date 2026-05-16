# GuildSpace

GuildSpace is a student-only UWA community web application designed to help students connect, share information, trade second-hand items, and interact with campus-related posts.

The application supports user registration and login, OTP verification, a community forum, a student marketplace, seller messaging, bidding, and persistent user-generated content.

---

## Purpose of the Application

The purpose of GuildSpace is to provide a central online platform for UWA students to:

* Browse campus-related posts and community notices
* Create forum posts and comments
* Buy and sell second-hand items through a marketplace
* Message sellers about marketplace listings
* Place bids on pending marketplace items
* Interact with content created by other students

GuildSpace is designed to be useful, accessible, and focused on the UWA student community.

---

## Main Features

### Authentication

* User registration with UWA student email validation
* OTP verification after registration
* Login and logout
* Password validation
* Passwords stored as salted hashes using Werkzeug
* Protected pages that require users to be logged in

### Home Page

* Full-width hero section
* Clear navigation to Forum, Marketplace, and Register pages
* Shared navbar and footer using Jinja templates
* Consistent layout and visual style across the site

### Forum

* Users can create forum posts
* Users can like and dislike posts
* Users can comment on posts
* Forum posts, likes, dislikes, and comments are persisted using SQLite through SQLAlchemy

### Marketplace

* Users can browse marketplace listings
* Users can create listings with images
* Users can message sellers
* Users can place bids on pending items
* Sellers can view messages and bids
* Sellers can update listing status
* Marketplace listings, messages, bids, and status updates are persisted using SQLite through SQLAlchemy

### Security

* CSRF token protection for POST forms
* Password hashing using Werkzeug
* UWA student email validation during registration
* Real mail credentials are excluded from GitHub using ignored local configuration files

---

## Design and Use

GuildSpace uses a Bootstrap-based layout with custom CSS. The visual design uses blue tones inspired by UWA branding and card-based sections to keep the interface clear and easy to use.

The main user flow is:

1. Register with a UWA student email
2. Verify email using OTP
3. Login
4. Use the Forum to create or interact with posts
5. Use the Marketplace to browse, post listings, message sellers, or place bids
6. Logout when finished

---

## Group Members

| UWA ID        | Name        | GitHub Username        |
| ------------- | ----------- | ---------------------- |
| 24231774 | Nikhil Chadha |  nikhilchadha28 |
| 23320288 | Zeyu Wang | zeyu-wang-123 |
| 24732787 | Sanchia Recson Lakkarvi | SanchiaLakkarvi |

---

## Technologies Used

* HTML
* CSS
* JavaScript
* Bootstrap
* Flask
* Jinja templates
* SQLite
* SQLAlchemy
* Flask-Mail
* Pytest
* Selenium

---

## Project Structure

```text
AgileWebDevelopment2026/
│
├── app.py
├── requirements.txt
├── README.md
├── TESTING.md
│
├── server/
│   ├── extensions.py
│   └── models/
│       ├── user.py
│       ├── post.py
│       └── marketplace.py
│
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
│
├── static/
│   ├── css/
│   ├── images/
│   └── pages/
│
├── tests/
│   ├── test_routes.py
│   └── test_selenium.py
│
└── docs/
    └── testing/
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SanchiaLakkarvi/AgileWebDevelopment2026.git
cd AgileWebDevelopment2026
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Configure email settings

The real email configuration file is not committed to GitHub for security reasons.

If OTP email sending is configured locally, create a `mail_config.py` file based on `mail_config_example.py`.

For local testing, OTP codes may also be printed in the Flask terminal.

---

## How to Launch the Application

Run the Flask application:

```bash
python3 app.py
```

Then open the application in a browser:

```text
http://127.0.0.1:5000
```

The application will create the local SQLite database automatically if it does not already exist.

---

## How to Run Unit Tests

Run the unit tests with:

```bash
python3 -m pytest tests/test_routes.py -v
```

The unit tests check core Flask route behaviour and password validation.

---

## How to Run Selenium Tests

Selenium tests require a live Flask server.

### Terminal 1: Start the Flask server

```bash
python3 app.py
```


### Terminal 2: Run Selenium tests

```bash
python3 -m pytest tests/test_selenium.py -v
```

The Selenium tests check browser-level behaviour such as login/register page loading and unauthenticated redirects.

---

## Manual Testing Evidence

Manual testing evidence is documented in:

```text
TESTING.md
```

Screenshots are stored in:

```text
docs/testing/
```

Manual testing covered:

- Register, OTP, login, and logout
- Homepage navigation
- Forum post, like, dislike, comment, and persistence
- Marketplace listing, message, bid, status update, and persistence
- Two-account buyer/seller flow
- CSRF-protected form submissions

---

## Notes on Local Data

Local database files and runtime data are ignored by Git and should not be committed.

Ignored local runtime files include:

```text
data/*.db
data/marketplace.json
static/images/uploads/*
```

This prevents local test data, uploaded files, and runtime database files from being accidentally pushed to GitHub.

---

## Known Future Improvements

Possible future improvements include:

- Adding a simple Profile page
- Adding a safe Delete Account flow
- Deciding how forum posts and marketplace listings should behave after account deletion
- Adding more detailed Selenium tests for logged-in user flows
- Improving deployment configuration for production use