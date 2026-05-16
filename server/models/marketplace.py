from datetime import datetime
from server.extensions import db


class MarketplaceItem(db.Model):
    __tablename__ = "marketplace_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False, default="placeholder-other.svg")
    seller = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Active")
    description = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(50), nullable=False, default="Just now")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class MarketplaceMessage(db.Model):
    __tablename__ = "marketplace_messages"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("marketplace_items.id"), nullable=False)
    item_title = db.Column(db.String(120), nullable=False)
    seller = db.Column(db.String(120), nullable=False)
    buyer_name = db.Column(db.String(120), nullable=False)
    buyer_email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class MarketplaceBid(db.Model):
    __tablename__ = "marketplace_bids"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("marketplace_items.id"), nullable=False)
    item_title = db.Column(db.String(120), nullable=False)
    seller = db.Column(db.String(120), nullable=False)
    buyer_name = db.Column(db.String(120), nullable=False)
    buyer_email = db.Column(db.String(120), nullable=False)
    bid_amount = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
