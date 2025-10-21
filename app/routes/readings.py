from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required, current_user
from datetime import datetime
import csv
from io import StringIO
from app import db
from app.models import BloodSugarReading

readings_bp = Blueprint('readings', __name__, url_prefix='/readings')

@readings_bp.route('/')
@login_required
def index():
    """List all readings"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    pagination = BloodSugarReading.query.filter_by(
        user_id=current_user.id
    ).order_by(BloodSugarReading.reading_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    readings = pagination.items

    return render_template(
        'readings/index.html',
        readings=readings,
        pagination=pagination
    )

@readings_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new reading"""
    if request.method == 'POST':
        try:
            value = float(request.form.get('value'))
            reading_time_str = request.form.get('reading_time')
            notes = request.form.get('notes', '')
            meal_context = request.form.get('meal_context', '')

            # Parse datetime
            if reading_time_str:
                reading_time = datetime.fromisoformat(reading_time_str)
            else:
                reading_time = datetime.utcnow()

            # Validate value
            if value <= 0 or value > 600:
                flash('Blood sugar value must be between 0 and 600 mg/dL.', 'error')
                return render_template('readings/add.html')

            # Create reading
            reading = BloodSugarReading(
                user_id=current_user.id,
                value=value,
                reading_time=reading_time,
                notes=notes,
                meal_context=meal_context
            )

            db.session.add(reading)
            db.session.commit()

            flash('Reading added successfully!', 'success')
            return redirect(url_for('readings.index'))

        except ValueError:
            flash('Invalid blood sugar value. Please enter a number.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the reading.', 'error')

    return render_template('readings/add.html')

@readings_bp.route('/<int:reading_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(reading_id):
    """Edit existing reading"""
    reading = BloodSugarReading.query.filter_by(
        id=reading_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == 'POST':
        try:
            reading.value = float(request.form.get('value'))
            reading_time_str = request.form.get('reading_time')
            reading.notes = request.form.get('notes', '')
            reading.meal_context = request.form.get('meal_context', '')

            if reading_time_str:
                reading.reading_time = datetime.fromisoformat(reading_time_str)

            # Validate value
            if reading.value <= 0 or reading.value > 600:
                flash('Blood sugar value must be between 0 and 600 mg/dL.', 'error')
                return render_template('readings/edit.html', reading=reading)

            db.session.commit()
            flash('Reading updated successfully!', 'success')
            return redirect(url_for('readings.index'))

        except ValueError:
            flash('Invalid blood sugar value. Please enter a number.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the reading.', 'error')

    return render_template('readings/edit.html', reading=reading)

@readings_bp.route('/<int:reading_id>/delete', methods=['POST'])
@login_required
def delete(reading_id):
    """Delete reading"""
    reading = BloodSugarReading.query.filter_by(
        id=reading_id,
        user_id=current_user.id
    ).first_or_404()

    try:
        db.session.delete(reading)
        db.session.commit()
        flash('Reading deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the reading.', 'error')

    return redirect(url_for('readings.index'))

@readings_bp.route('/export')
@login_required
def export():
    """Export readings to CSV"""
    readings = BloodSugarReading.query.filter_by(
        user_id=current_user.id
    ).order_by(BloodSugarReading.reading_time.desc()).all()

    # Create CSV
    si = StringIO()
    writer = csv.writer(si)

    # Write header
    writer.writerow(['Date & Time', 'Blood Sugar (mg/dL)', 'Meal Context', 'Notes', 'Status', 'Recommendation'])

    # Write data
    for reading in readings:
        status = BloodSugarReading.get_status(reading.value)
        recommendation = reading.get_recommendation()

        writer.writerow([
            reading.reading_time.strftime('%Y-%m-%d %H:%M:%S'),
            reading.value,
            reading.meal_context or 'N/A',
            reading.notes or '',
            status,
            recommendation
        ])

    # Create response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=blood_sugar_readings_{datetime.now().strftime('%Y%m%d')}.csv"
    output.headers["Content-type"] = "text/csv"

    return output

@readings_bp.route('/api/recent')
@login_required
def api_recent():
    """API endpoint for recent readings (for charts)"""
    days = request.args.get('days', 30, type=int)

    from datetime import timedelta
    start_date = datetime.utcnow() - timedelta(days=days)

    readings = BloodSugarReading.query.filter(
        BloodSugarReading.user_id == current_user.id,
        BloodSugarReading.reading_time >= start_date
    ).order_by(BloodSugarReading.reading_time.asc()).all()

    data = [{
        'date': r.reading_time.strftime('%Y-%m-%d %H:%M'),
        'value': r.value,
        'status': BloodSugarReading.get_status(r.value)
    } for r in readings]

    return jsonify(data)
