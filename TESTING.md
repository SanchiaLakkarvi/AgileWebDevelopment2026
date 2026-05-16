# Testing Evidence

Manual regression testing was completed on the latest `main` branch.

## Environment

- Local server: `python3 app.py`
- Browser: Chrome
- Database: SQLite with SQLAlchemy

## Manual Testing

### Register validation

Tested register form validation, including password requirement checking.

![Register validation](docs/testing/register-validation.png)

### Home page navigation

Tested homepage layout, clickable cards, Get Started button, and footer display.

![Home page](docs/testing/home-page.png)

### Forum persistence

Tested forum post creation, like/dislike, comment, refresh, and server restart persistence.

![Forum persistence](docs/testing/forum-persistence.png)

### Marketplace persistence

Tested marketplace listing creation, status update, refresh, and server restart persistence.

![Marketplace persistence](docs/testing/marketplace-persistence.png)

### Message seller

Tested two-account message seller flow and confirmed the seller can view messages in Inbox.

![Inbox message](docs/testing/inbox-message.png)

### Place bid

Tested two-account bid flow and confirmed the seller can view bids in the Bids page.

![Bids page](docs/testing/bids-page.png)

## Result

All core manual testing flows passed.