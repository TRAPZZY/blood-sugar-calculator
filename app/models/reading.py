from datetime import datetime
from app import db

class BloodSugarReading(db.Model):
    """Blood sugar reading model"""
    __tablename__ = 'blood_sugar_readings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    reading_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text)
    meal_context = db.Column(db.String(50))  # before_meal, after_meal, fasting, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BloodSugarReading {self.value} at {self.reading_time}>'

    def to_dict(self):
        """Convert reading to dictionary"""
        return {
            'id': self.id,
            'value': self.value,
            'reading_time': self.reading_time.isoformat(),
            'notes': self.notes,
            'meal_context': self.meal_context,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def get_status(value):
        """Get status based on blood sugar value"""
        if value < 70:
            return 'critical_low'
        elif value < 100:
            return 'low'
        elif value <= 130:
            return 'normal'
        elif value <= 150:
            return 'elevated'
        else:
            return 'high'

    def get_recommendation(self):
        """Get recommendation based on reading value"""
        status = self.get_status(self.value)

        recommendations = {
            'critical_low': 'Your blood sugar is critically low. Consume fast-acting carbohydrates immediately and seek medical attention if symptoms persist.',
            'low': 'Your blood sugar is below normal. Consider adjusting your diet to include more complex carbohydrates.',
            'normal': 'Your blood sugar is in the healthy range. Keep up the good work!',
            'elevated': 'Your blood sugar is slightly elevated. Monitor your diet and consider more physical activity.',
            'high': 'Your blood sugar is high. Consult with your healthcare provider for personalized advice and medication if needed.'
        }

        return recommendations.get(status, 'Unable to determine recommendation')

    def get_meal_suggestion(self):
        """Get meal suggestion based on reading value"""
        status = self.get_status(self.value)

        suggestions = {
            'critical_low': 'Immediately consume 15-20g of fast-acting carbs (juice, glucose tablets). Follow with a balanced snack.',
            'low': 'Opt for a meal rich in complex carbohydrates, lean proteins, and healthy fats to stabilize blood sugar.',
            'normal': 'Enjoy a well-balanced meal with a variety of nutrients including whole grains, vegetables, and lean protein.',
            'elevated': 'Choose high-fiber foods, non-starchy vegetables, and lean proteins. Limit simple carbohydrates.',
            'high': 'Focus on non-starchy vegetables, lean proteins, and avoid sugary foods and refined carbohydrates.'
        }

        return suggestions.get(status, 'Consult with a nutritionist for personalized meal planning')
