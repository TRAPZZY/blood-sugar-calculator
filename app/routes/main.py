from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models import BloodSugarReading, Goal, Reminder

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get recent readings (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_readings = BloodSugarReading.query.filter(
        BloodSugarReading.user_id == current_user.id,
        BloodSugarReading.reading_time >= seven_days_ago
    ).order_by(BloodSugarReading.reading_time.desc()).all()

    # Calculate statistics
    stats = {}
    if recent_readings:
        values = [r.value for r in recent_readings]
        stats = {
            'average': round(sum(values) / len(values), 1),
            'min': min(values),
            'max': max(values),
            'count': len(values)
        }

        # Determine trend
        if len(values) >= 2:
            first_half = values[:len(values)//2]
            second_half = values[len(values)//2:]
            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)

            if avg_second > avg_first + 5:
                stats['trend'] = 'increasing'
            elif avg_second < avg_first - 5:
                stats['trend'] = 'decreasing'
            else:
                stats['trend'] = 'stable'
        else:
            stats['trend'] = 'insufficient_data'
    else:
        stats = {
            'average': 0,
            'min': 0,
            'max': 0,
            'count': 0,
            'trend': 'no_data'
        }

    # Get active goals
    active_goals = Goal.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).all()

    # Get latest reading
    latest_reading = BloodSugarReading.query.filter_by(
        user_id=current_user.id
    ).order_by(BloodSugarReading.reading_time.desc()).first()

    # Get reminder settings
    reminder = Reminder.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()

    return render_template(
        'dashboard.html',
        recent_readings=recent_readings[:10],  # Show last 10
        stats=stats,
        active_goals=active_goals,
        latest_reading=latest_reading,
        reminder=reminder
    )

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    total_readings = BloodSugarReading.query.filter_by(
        user_id=current_user.id
    ).count()

    total_goals = Goal.query.filter_by(
        user_id=current_user.id
    ).count()

    # Get first reading date
    first_reading = BloodSugarReading.query.filter_by(
        user_id=current_user.id
    ).order_by(BloodSugarReading.reading_time.asc()).first()

    days_tracking = 0
    if first_reading:
        days_tracking = (datetime.utcnow() - first_reading.reading_time).days

    return render_template(
        'profile.html',
        total_readings=total_readings,
        total_goals=total_goals,
        days_tracking=days_tracking
    )
