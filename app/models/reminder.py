from datetime import datetime
from app import db

class Reminder(db.Model):
    """Reminder settings for users"""
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interval_hours = db.Column(db.Integer, nullable=False, default=4)
    is_active = db.Column(db.Boolean, default=True)
    last_reminded_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Reminder every {self.interval_hours}h for user {self.user_id}>'

    def to_dict(self):
        """Convert reminder to dictionary"""
        return {
            'id': self.id,
            'interval_hours': self.interval_hours,
            'is_active': self.is_active,
            'last_reminded_at': self.last_reminded_at.isoformat() if self.last_reminded_at else None,
            'created_at': self.created_at.isoformat()
        }
