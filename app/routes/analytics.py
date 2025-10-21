from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
import numpy as np
from app import db
from app.models import BloodSugarReading, Goal

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
@login_required
def index():
    """Analytics dashboard"""
    return render_template('analytics/index.html')

@analytics_bp.route('/trends')
@login_required
def trends():
    """View detailed trends"""
    # Get all readings
    readings = BloodSugarReading.query.filter_by(
        user_id=current_user.id
    ).order_by(BloodSugarReading.reading_time.asc()).all()

    if not readings:
        return render_template('analytics/trends.html', has_data=False)

    # Calculate statistics
    values = [r.value for r in readings]

    stats = {
        'total_readings': len(values),
        'average': round(sum(values) / len(values), 1),
        'min': min(values),
        'max': max(values),
        'std_dev': round(np.std(values), 1) if len(values) > 1 else 0
    }

    # Analyze trend
    if len(values) >= 2:
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)

        if avg_second > avg_first + 5:
            stats['trend'] = 'Blood sugar is increasing over time'
            stats['trend_type'] = 'increasing'
        elif avg_second < avg_first - 5:
            stats['trend'] = 'Blood sugar is decreasing over time'
            stats['trend_type'] = 'decreasing'
        else:
            stats['trend'] = 'Blood sugar is relatively stable'
            stats['trend_type'] = 'stable'
    else:
        stats['trend'] = 'Insufficient data to detect trends'
        stats['trend_type'] = 'insufficient'

    # Distribution analysis
    critical_low = sum(1 for v in values if v < 70)
    low = sum(1 for v in values if 70 <= v < 100)
    normal = sum(1 for v in values if 100 <= v <= 130)
    elevated = sum(1 for v in values if 130 < v <= 150)
    high = sum(1 for v in values if v > 150)

    distribution = {
        'critical_low': critical_low,
        'low': low,
        'normal': normal,
        'elevated': elevated,
        'high': high
    }

    return render_template(
        'analytics/trends.html',
        has_data=True,
        stats=stats,
        distribution=distribution
    )

@analytics_bp.route('/compare-weeks')
@login_required
def compare_weeks():
    """Compare blood sugar trends between weeks"""
    # Get readings from last 4 weeks
    four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)

    readings = BloodSugarReading.query.filter(
        BloodSugarReading.user_id == current_user.id,
        BloodSugarReading.reading_time >= four_weeks_ago
    ).order_by(BloodSugarReading.reading_time.asc()).all()

    if not readings:
        return render_template('analytics/compare_weeks.html', has_data=False)

    # Group readings by week
    weeks_data = {}
    for reading in readings:
        week_num = (datetime.utcnow() - reading.reading_time).days // 7
        week_label = f"Week {4 - week_num}" if week_num < 4 else "Older"

        if week_label not in weeks_data:
            weeks_data[week_label] = []

        weeks_data[week_label].append(reading.value)

    # Calculate averages for each week
    weeks_summary = {}
    for week, values in weeks_data.items():
        if values:
            weeks_summary[week] = {
                'average': round(sum(values) / len(values), 1),
                'min': min(values),
                'max': max(values),
                'count': len(values)
            }

    return render_template(
        'analytics/compare_weeks.html',
        has_data=True,
        weeks_summary=weeks_summary
    )

@analytics_bp.route('/predictions')
@login_required
def predictions():
    """Blood sugar predictions using linear regression"""
    # Get all readings
    readings = BloodSugarReading.query.filter_by(
        user_id=current_user.id
    ).order_by(BloodSugarReading.reading_time.asc()).all()

    if len(readings) < 5:
        return render_template(
            'analytics/predictions.html',
            has_data=False,
            message="Need at least 5 readings for predictions"
        )

    # Prepare data for linear regression
    values = [r.value for r in readings]
    x = np.arange(len(values))

    # Calculate linear regression
    coefficients = np.polyfit(x, values, 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    # Make predictions for next 7 days (assuming 3 readings per day)
    future_points = 21  # 7 days * 3 readings
    future_x = np.arange(len(values), len(values) + future_points)
    predictions = slope * future_x + intercept

    # Calculate confidence
    r_squared = 1 - (sum((np.array(values) - (slope * x + intercept))**2) / sum((np.array(values) - np.mean(values))**2))

    prediction_summary = {
        'slope': round(slope, 3),
        'trend': 'increasing' if slope > 0.1 else 'decreasing' if slope < -0.1 else 'stable',
        'confidence': round(r_squared * 100, 1),
        'next_week_avg': round(np.mean(predictions), 1),
        'predictions': [round(p, 1) for p in predictions[:7]]  # Show first 7 predictions
    }

    return render_template(
        'analytics/predictions.html',
        has_data=True,
        prediction_summary=prediction_summary
    )

@analytics_bp.route('/api/chart-data')
@login_required
def api_chart_data():
    """API endpoint for chart data"""
    chart_type = request.args.get('type', 'line')
    days = request.args.get('days', 30, type=int)

    start_date = datetime.utcnow() - timedelta(days=days)

    readings = BloodSugarReading.query.filter(
        BloodSugarReading.user_id == current_user.id,
        BloodSugarReading.reading_time >= start_date
    ).order_by(BloodSugarReading.reading_time.asc()).all()

    if chart_type == 'line':
        # Line chart data
        data = {
            'labels': [r.reading_time.strftime('%Y-%m-%d %H:%M') for r in readings],
            'values': [r.value for r in readings]
        }
    elif chart_type == 'distribution':
        # Distribution chart data
        values = [r.value for r in readings]
        data = {
            'critical_low': sum(1 for v in values if v < 70),
            'low': sum(1 for v in values if 70 <= v < 100),
            'normal': sum(1 for v in values if 100 <= v <= 130),
            'elevated': sum(1 for v in values if 130 < v <= 150),
            'high': sum(1 for v in values if v > 150)
        }
    elif chart_type == 'weekly':
        # Weekly average chart
        weeks = {}
        for reading in readings:
            week_start = reading.reading_time - timedelta(days=reading.reading_time.weekday())
            week_key = week_start.strftime('%Y-%m-%d')

            if week_key not in weeks:
                weeks[week_key] = []
            weeks[week_key].append(reading.value)

        data = {
            'labels': list(weeks.keys()),
            'values': [round(sum(v) / len(v), 1) for v in weeks.values()]
        }
    else:
        data = {'error': 'Invalid chart type'}

    return jsonify(data)

@analytics_bp.route('/api/goals-progress')
@login_required
def api_goals_progress():
    """API endpoint for goals progress"""
    goals = Goal.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).all()

    # Get recent readings (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    readings = BloodSugarReading.query.filter(
        BloodSugarReading.user_id == current_user.id,
        BloodSugarReading.reading_time >= thirty_days_ago
    ).all()

    progress_data = []
    for goal in goals:
        in_range = sum(1 for r in readings if goal.is_in_range(r.value))
        total = len(readings)

        progress_data.append({
            'name': goal.name,
            'target_min': goal.target_min,
            'target_max': goal.target_max,
            'in_range': in_range,
            'total': total,
            'percentage': round((in_range / total * 100) if total > 0 else 0, 1)
        })

    return jsonify(progress_data)
