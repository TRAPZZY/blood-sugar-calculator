# Blood Sugar Monitor - Web Application

A comprehensive, production-ready web application for tracking and analyzing blood sugar levels with personalized insights, goal setting, and advanced analytics.

## Features

### Core Functionality
- **User Authentication & Personalization**: Secure user registration and login with personalized dashboards
- **Blood Sugar Tracking**: Record and manage blood sugar readings with timestamps, meal context, and notes
- **Goal Setting**: Define custom target ranges and track progress towards health goals
- **Trend Analysis**: Analyze blood sugar patterns with statistical insights and visualizations
- **Predictions**: Forecast future blood sugar levels using linear regression
- **Weekly Comparisons**: Compare blood sugar trends across different weeks
- **Meal Suggestions**: Get personalized meal recommendations based on readings
- **CSV Export**: Download all your data for sharing with healthcare providers
- **Reminder System**: Configure reminders for consistent tracking

### Technical Features
- **Full-Stack Web Application**: Flask backend with responsive HTML/CSS/JavaScript frontend
- **Database Persistence**: SQLite database with SQLAlchemy ORM
- **Data Visualization**: Interactive charts using Chart.js
- **HIPAA Compliant**: Secure handling of health data
- **RESTful API**: Clean API endpoints for data operations
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

4. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### Getting Started

1. **Register an Account**:
   - Navigate to the registration page
   - Provide your name, username, email, and password
   - Click "Register" to create your account

2. **Login**:
   - Use your username and password to log in
   - Access your personalized dashboard

3. **Add Your First Reading**:
   - Click "Add New Reading" on the dashboard
   - Enter your blood sugar value (mg/dL)
   - Select meal context (optional)
   - Add any notes (optional)
   - Click "Save Reading"

4. **Set Health Goals**:
   - Navigate to "Goals" in the menu
   - Click "Add New Goal"
   - Define your target blood sugar range
   - Track your progress over time

5. **View Analytics**:
   - Navigate to "Analytics" to see:
     - Trend analysis and patterns
     - Weekly comparisons
     - Predictions for future readings
     - Distribution charts

### Features Guide

#### Dashboard
Your personalized dashboard shows:
- 7-day average blood sugar
- Total readings in the last week
- Latest reading with status and recommendations
- Active health goals
- Recent readings table
- Quick action buttons

#### Blood Sugar Readings
- **Add Reading**: Record new blood sugar measurements
- **View All**: See complete history with pagination
- **Edit**: Update existing readings
- **Delete**: Remove incorrect entries
- **Export**: Download data as CSV

#### Goals
- **Create Goals**: Set custom target ranges (e.g., "Normal Range: 100-130 mg/dL")
- **Track Progress**: Monitor how often readings fall within goals
- **Activate/Deactivate**: Enable or disable goals as needed

#### Analytics
- **Trends**: View overall statistics, distribution, and patterns
- **Compare Weeks**: Analyze week-to-week changes
- **Predictions**: Forecast future levels using linear regression
- **Charts**: Interactive visualizations with Chart.js

#### Reminders
- Configure reminder intervals (1-24 hours)
- Enable/disable reminders as needed
- Stay consistent with tracking

## Blood Sugar Ranges

### Status Classification
- **Critical Low**: Below 70 mg/dL - Immediate attention needed
- **Low**: 70-99 mg/dL - Below normal range
- **Normal**: 100-130 mg/dL - Healthy range
- **Elevated**: 131-150 mg/dL - Slightly elevated
- **High**: Above 150 mg/dL - Consult healthcare provider

### Recommended Targets
- **Fasting/Before Meals**: 80-130 mg/dL
- **1-2 Hours After Meals**: Less than 180 mg/dL
- **Bedtime**: 90-150 mg/dL

*Note: These are general guidelines. Consult your healthcare provider for personalized targets.*

## Project Structure

```
blood-sugar-calculator/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models/                  # Database models
│   │   ├── user.py             # User authentication model
│   │   ├── reading.py          # Blood sugar readings model
│   │   ├── goal.py             # Health goals model
│   │   └── reminder.py         # Reminder settings model
│   ├── routes/                  # Application routes
│   │   ├── auth.py             # Authentication routes
│   │   ├── main.py             # Main dashboard routes
│   │   ├── readings.py         # Reading management routes
│   │   ├── goals.py            # Goals and reminders routes
│   │   └── analytics.py        # Analytics and predictions routes
│   ├── templates/               # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Landing page
│   │   ├── dashboard.html      # User dashboard
│   │   ├── auth/               # Authentication templates
│   │   ├── readings/           # Reading templates
│   │   ├── goals/              # Goals templates
│   │   └── analytics/          # Analytics templates
│   └── static/                  # Static assets
│       ├── css/
│       │   └── style.css       # Application styles
│       └── js/
│           └── main.js         # JavaScript functionality
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── run.py                       # Application runner
└── README_WEB_APP.md           # This file
```

## Configuration

### Environment Variables
You can customize the application using environment variables:

- `SECRET_KEY`: Flask secret key for sessions (default: auto-generated)
- `DATABASE_URL`: Database connection URL (default: SQLite)

### Application Settings
Edit `config.py` to modify:
- Blood sugar thresholds
- Session timeout
- Database settings
- Security options

## Database

The application uses SQLite by default, storing data in `blood_sugar.db`. The database includes:

- **Users**: User accounts and authentication
- **Blood Sugar Readings**: All recorded measurements
- **Goals**: User-defined target ranges
- **Reminders**: Notification settings

## Security Features

- Password hashing using Werkzeug
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Secure user authentication
- Data isolation per user
- HIPAA-compliant data handling

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout

### Readings
- `GET /readings/` - List all readings
- `GET /readings/add` - Add reading form
- `POST /readings/add` - Create reading
- `GET /readings/<id>/edit` - Edit reading form
- `POST /readings/<id>/edit` - Update reading
- `POST /readings/<id>/delete` - Delete reading
- `GET /readings/export` - Export to CSV
- `GET /readings/api/recent` - Get recent readings (JSON)

### Goals
- `GET /goals/` - List all goals
- `POST /goals/add` - Create goal
- `POST /goals/<id>/edit` - Update goal
- `POST /goals/<id>/delete` - Delete goal
- `GET /goals/reminders` - Reminder settings
- `POST /goals/reminders` - Update reminders

### Analytics
- `GET /analytics/` - Analytics dashboard
- `GET /analytics/trends` - Trend analysis
- `GET /analytics/compare-weeks` - Weekly comparison
- `GET /analytics/predictions` - Blood sugar predictions
- `GET /analytics/api/chart-data` - Chart data (JSON)
- `GET /analytics/api/goals-progress` - Goals progress (JSON)

## Production Deployment

### Preparation
1. Set a strong `SECRET_KEY` environment variable
2. Use PostgreSQL or MySQL instead of SQLite
3. Enable HTTPS/SSL
4. Set `debug=False` in production
5. Use a production WSGI server (gunicorn, uwsgi)

### Example with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Troubleshooting

### Database Issues
- Delete `blood_sugar.db` and restart to reset database
- Check file permissions on database file

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+)

### Port Already in Use
- Change port in `run.py`: `app.run(port=5001)`

## Contributing

This is a personal health tracking application. For improvements:
1. Test changes thoroughly
2. Maintain HIPAA compliance
3. Document new features
4. Follow existing code style

## Disclaimer

**IMPORTANT**: This application is for informational and tracking purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers regarding your health conditions and blood sugar management.

## License

This project is provided as-is for personal use.

## Support

For issues or questions:
1. Check this README
2. Review the application logs
3. Verify all dependencies are installed
4. Ensure database permissions are correct

## Changelog

### Version 1.0.0 (2024)
- Initial release of web application
- User authentication and personalization
- Blood sugar tracking with full CRUD operations
- Goal setting and tracking
- Advanced analytics and predictions
- CSV export functionality
- Responsive web design
- Chart.js visualizations
- Reminder system
- HIPAA-compliant data handling

---

**Built with**: Flask, SQLAlchemy, Chart.js, and modern web technologies.
