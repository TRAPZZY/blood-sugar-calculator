from datetime import datetime
from app import db

class Goal(db.Model):
    """User health goals model"""
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    target_min = db.Column(db.Float, nullable=False)
    target_max = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Goal {self.name}: {self.target_min}-{self.target_max}>'

    def to_dict(self):
        """Convert goal to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'target_min': self.target_min,
            'target_max': self.target_max,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def is_in_range(self, value):
        """Check if a value is within goal range"""
        return self.target_min <= value <= self.target_max
