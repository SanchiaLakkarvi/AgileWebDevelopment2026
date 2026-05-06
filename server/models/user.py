from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

from server.extensions import db


class User(db.Model):
    #Creating database to save registered user details

    __tablename__ = "register_data"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    dob = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    hashed_password = db.Column(db.String(255), nullable=False)

    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    otp_number = db.Column(db.String(6), nullable=True)
    otp_generation_time = db.Column(db.DateTime, nullable=True)

    account_generation_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    #Joining first name and last name
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)