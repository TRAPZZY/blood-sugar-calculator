# Quick Start Guide - Blood Sugar Monitor

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python run.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

---

## 📝 First-Time Setup

1. **Register Your Account**
   - Click "Get Started" or "Register"
   - Fill in your information
   - Create a strong password

2. **Log In**
   - Use your username and password
   - Check "Remember me" for convenience

3. **Add Your First Reading**
   - Click "Add New Reading"
   - Enter your blood sugar value
   - Click "Save Reading"

4. **Explore Features**
   - View your Dashboard
   - Set health Goals
   - Check Analytics

---

## 🎯 Key Features at a Glance

### Dashboard
- See your 7-day average
- View latest reading with recommendations
- Quick action buttons

### Readings
- Add, edit, delete readings
- Export to CSV
- Filter by date

### Goals
- Set target ranges
- Track progress
- Get personalized advice

### Analytics
- View trends
- Compare weeks
- See predictions

---

## 🐳 Docker Quick Start

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Using Docker
```bash
docker build -t blood-sugar-monitor .
docker run -p 5000:5000 blood-sugar-monitor
```

---

## 💡 Tips

- **First Reading**: Add at least 5 readings to see trends
- **Goals**: Set realistic target ranges with your doctor
- **Consistency**: Track regularly for best insights
- **Export**: Download CSV to share with healthcare providers
- **Reminders**: Set up reminders for consistent tracking

---

## ⚠️ Troubleshooting

### Port Already in Use
```bash
# Change port in run.py or use:
python run.py --port 5001
```

### Dependencies Not Installing
```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

### Database Errors
```bash
# Reset database (WARNING: Deletes all data)
rm blood_sugar.db
python run.py
```

---

## 📊 Blood Sugar Ranges Reference

| Status | Range (mg/dL) | Action |
|--------|---------------|--------|
| Critical Low | < 70 | Immediate attention |
| Low | 70-99 | Below normal |
| Normal | 100-130 | Healthy range |
| Elevated | 131-150 | Monitor closely |
| High | > 150 | Consult doctor |

---

## 🔒 Security Note

- Change the `SECRET_KEY` in production
- Use strong passwords
- Never share your login credentials
- Enable HTTPS in production

---

## 📚 Need More Help?

See `README_WEB_APP.md` for complete documentation.

---

**Enjoy tracking your health!** 🏥📈
