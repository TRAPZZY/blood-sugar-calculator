from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Goal, BloodSugarReading, Reminder
from datetime import datetime

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route('/')
@login_required
def index():
    """List all goals"""
    goals = Goal.query.filter_by(
        user_id=current_user.id
    ).order_by(Goal.created_at.desc()).all()

    return render_template('goals/index.html', goals=goals)

@goals_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new goal"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            target_min = float(request.form.get('target_min'))
            target_max = float(request.form.get('target_max'))

            # Validation
            if not name:
                flash('Goal name is required.', 'error')
                return render_template('goals/add.html')

            if target_min >= target_max:
                flash('Target minimum must be less than target maximum.', 'error')
                return render_template('goals/add.html')

            if target_min < 0 or target_max > 600:
                flash('Target values must be between 0 and 600 mg/dL.', 'error')
                return render_template('goals/add.html')

            # Create goal
            goal = Goal(
                user_id=current_user.id,
                name=name,
                target_min=target_min,
                target_max=target_max,
                is_active=True
            )

            db.session.add(goal)
            db.session.commit()

            flash('Goal created successfully!', 'success')
            return redirect(url_for('goals.index'))

        except ValueError:
            flash('Invalid target values. Please enter valid numbers.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the goal.', 'error')

    return render_template('goals/add.html')

@goals_bp.route('/<int:goal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(goal_id):
    """Edit existing goal"""
    goal = Goal.query.filter_by(
        id=goal_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == 'POST':
        try:
            goal.name = request.form.get('name')
            goal.target_min = float(request.form.get('target_min'))
            goal.target_max = float(request.form.get('target_max'))
            goal.is_active = request.form.get('is_active') == 'on'

            # Validation
            if not goal.name:
                flash('Goal name is required.', 'error')
                return render_template('goals/edit.html', goal=goal)

            if goal.target_min >= goal.target_max:
                flash('Target minimum must be less than target maximum.', 'error')
                return render_template('goals/edit.html', goal=goal)

            if goal.target_min < 0 or goal.target_max > 600:
                flash('Target values must be between 0 and 600 mg/dL.', 'error')
                return render_template('goals/edit.html', goal=goal)

            db.session.commit()
            flash('Goal updated successfully!', 'success')
            return redirect(url_for('goals.index'))

        except ValueError:
            flash('Invalid target values. Please enter valid numbers.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the goal.', 'error')

    return render_template('goals/edit.html', goal=goal)

@goals_bp.route('/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete(goal_id):
    """Delete goal"""
    goal = Goal.query.filter_by(
        id=goal_id,
        user_id=current_user.id
    ).first_or_404()

    try:
        db.session.delete(goal)
        db.session.commit()
        flash('Goal deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the goal.', 'error')

    return redirect(url_for('goals.index'))

@goals_bp.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    """Manage reminder settings"""
    reminder = Reminder.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == 'POST':
        try:
            interval_hours = int(request.form.get('interval_hours'))
            is_active = request.form.get('is_active') == 'on'

            # Validation
            if interval_hours < 1 or interval_hours > 24:
                flash('Reminder interval must be between 1 and 24 hours.', 'error')
                return render_template('goals/reminders.html', reminder=reminder)

            if reminder:
                # Update existing reminder
                reminder.interval_hours = interval_hours
                reminder.is_active = is_active
            else:
                # Create new reminder
                reminder = Reminder(
                    user_id=current_user.id,
                    interval_hours=interval_hours,
                    is_active=is_active
                )
                db.session.add(reminder)

            db.session.commit()
            flash('Reminder settings updated successfully!', 'success')
            return redirect(url_for('goals.reminders'))

        except ValueError:
            flash('Invalid interval value. Please enter a valid number.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating reminder settings.', 'error')

    return render_template('goals/reminders.html', reminder=reminder)
