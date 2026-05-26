# Skill Decay Tracker

A simple, beginner-friendly web application to track your technical skills and monitor whether they're improving or weakening over time based on your practice activity.

## 📋 Project Overview

The **Skill Decay Tracker** helps students and developers:
- **Track skills** they're learning and developing
- **Log practice sessions** to stay consistent
- **Monitor skill strength** based on a simple decay formula
- **Visualize progress** with an analytics dashboard
- **Get alerts** when skills haven't been practiced recently

The app uses a simple formula to simulate "skill decay" - the more time you go without practicing, the weaker your skill becomes. By logging practice sessions regularly, you can maintain and improve your skill strength.

## ✨ Features

### 1. User Authentication
- Sign up for a new account
- Login with username and password
- Secure session-based authentication
- Logout functionality

### 2. Skill Management
- Add new skills to track
- Edit skill details (name and level)
- Delete skills you no longer want to track
- View all your skills at a glance
- Skills are categorized by level: Beginner, Intermediate, Advanced

### 3. Practice Logging
- Log practice sessions for each skill
- Record hours practiced
- Add activity descriptions (optional)
- Track practice date
- View full history of practice logs

### 4. Skill Strength Calculation
The app calculates skill strength using a simple formula:

```
Skill Strength = 100 - (inactive days × 1) + (recent practice bonus)
```

**Scoring:**
- Start with base score of 100
- Lose 1 point for each day without practice
- Gain 2 points for each hour practiced in the last 30 days
- Score is capped between 0-100
- Minimum: 0, Maximum: 100

**Strength Levels:**
- 🟢 **Strong** (70-100): Keep it up!
- 🟡 **At Risk** (40-69): Time to practice
- 🔴 **Critical** (0-39): Needs immediate attention

### 5. Dashboard & Analytics
- View total skills count
- See strongest and weakest skills
- Check average strength across all skills
- View recent practice activity
- Visual bar chart showing all skills' strength
- Get alerts for skills needing practice

### 6. Warning System
The app shows warnings when:
- A skill hasn't been practiced for 7+ days
- Skill strength drops below 40
- Helps you stay consistent with your learning

## 🛠️ Technologies Used

### Backend
- **Framework:** Flask (Python web framework)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Flask session + password hashing

### Frontend
- **HTML5:** For page structure
- **CSS3:** Custom responsive styling
- **Bootstrap 5:** For responsive UI components
- **JavaScript:** Vanilla JS for interactivity
- **Chart.js:** For data visualization (bar charts)

### Dependencies
- Flask 2.3.2
- Flask-SQLAlchemy 3.0.5
- SQLAlchemy 2.0.19
- Werkzeug 2.3.6

## 📁 Project Structure

```
skill_decay_tracker/
│
├── app.py                      # Main Flask application with all routes
├── models.py                   # Database models (User, Skill, PracticeLog)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template (navigation, layout)
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard with analytics
│   ├── skills.html            # Skills list view
│   ├── add_skill.html         # Add new skill form
│   ├── edit_skill.html        # Edit skill form
│   ├── skill_detail.html      # Skill details and practice logs
│   ├── log_practice.html      # Log practice session form
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styling
│   └── js/                    # JavaScript files (if needed)
│
└── skill_decay_tracker.db     # SQLite database (created on first run)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or download** the project:
   ```bash
   cd skill_decay_tracker
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📖 How to Use

### Step 1: Create an Account
- Click "Register" button
- Enter username, email, and password
- Click "Create Account"

### Step 2: Add Your First Skill
- Click "Add Skill" in the navbar
- Enter skill name (e.g., "Python", "React", "Docker")
- Select your current level
- Choose the date you started learning
- Click "Add Skill"

### Step 3: Log Practice Sessions
- Go to your Skills list
- Click "Log Practice" on any skill
- Enter practice date, hours, and activity description
- Click "Log Practice"

### Step 4: Monitor Your Progress
- Check the **Dashboard** to see all your skills
- View **Skill Details** for a specific skill
- Watch the strength bar and get alerts for skills needing practice

### Step 5: Maintain Your Skills
- Practice regularly to keep your skills strong
- Log each practice session
- Watch your skill strength improve!

## 📊 Dashboard Features

The dashboard shows:
- **Total Skills:** How many skills you're tracking
- **Average Strength:** Overall average strength across all skills
- **Strongest & Weakest Skills:** Quick glance at your best and worst skills
- **Skill Chart:** Visual bar chart of all skills with color coding
- **Recent Activity:** Last 10 practice sessions logged
- **Skill Warnings:** Skills that need attention (not practiced in 7+ days or strength < 40)

## 🎨 User Interface

The app features a **clean, beginner-friendly interface** with:
- Simple navigation bar
- Bootstrap 5 components (cards, forms, buttons)
- Responsive design (works on mobile and desktop)
- Color-coded skill strength (Green/Yellow/Red)
- Easy-to-read alert messages
- Intuitive forms with validation

## 💾 Database Schema

### Users Table
```sql
id (Primary Key)
username (Unique)
email (Unique)
password (Hashed)
created_at
```

### Skills Table
```sql
id (Primary Key)
user_id (Foreign Key → Users)
skill_name
level (Beginner/Intermediate/Advanced)
learning_date
created_at
```

### Practice Logs Table
```sql
id (Primary Key)
skill_id (Foreign Key → Skills)
hours_practiced
activity_description
practice_date
created_at
```

## 🧮 Skill Strength Algorithm

The skill strength calculation considers:

1. **Inactivity Penalty:** -1 point per day without practice
2. **Practice Bonus:** +2 points per hour practiced in last 30 days
3. **Base Score:** 100 points
4. **Bounds:** Always between 0 and 100

Example:
- A skill with 20 days of inactivity and 5 hours of practice in the last 30 days:
  - Strength = 100 - (20 × 1) + (5 × 2) = 100 - 20 + 10 = **90/100** ✓

## 🔒 Security Notes

This is a student project. For production use, consider:
- Using environment variables for the Flask secret key
- Implementing stronger password requirements
- Adding HTTPS/SSL
- Using a more robust database (PostgreSQL)
- Adding CSRF protection
- Implementing password reset functionality
- Adding email verification

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure you've activated your virtual environment and installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Database locked
**Solution:** Delete `skill_decay_tracker.db` and restart the app to create a fresh database

### Issue: Port 5000 already in use
**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

## 📝 Future Enhancements

Possible features to add:
- Email notifications for practice reminders
- Skill difficulty levels (bronze, silver, gold)
- Skill recommendations
- Study goals and milestones
- Export practice logs to CSV
- Dark mode
- Multiple practice categories per skill
- Time-based statistics and trends

## 📚 Learning Resources

This project uses:
- **Flask:** [Flask Documentation](https://flask.palletsprojects.com/)
- **SQLAlchemy:** [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- **Bootstrap:** [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- **Chart.js:** [Chart.js Documentation](https://www.chartjs.org/)

## 👨‍💻 Code Style

The code is written to be:
- **Beginner-friendly:** Easy to understand for college students
- **Well-commented:** Explanations throughout the code
- **Realistic:** Like a genuine student project, not overengineered
- **Practical:** Uses common Python and Flask patterns
- **Clean:** Organized file structure and clear naming

## 📄 License

This project is free to use for learning and educational purposes.

## 🎓 About This Project

This is a student project created to demonstrate:
- Full-stack web development basics
- Flask framework fundamentals
- Database modeling with SQLAlchemy
- HTML/CSS/Bootstrap frontend
- User authentication and session management
- Data visualization with Chart.js
- Responsive web design

Perfect for:
- College portfolio projects
- Internship interview discussions
- Learning web development
- Teaching beginners about full-stack apps

## 📧 Support

If you have questions or issues:
1. Check the Troubleshooting section
2. Review the code comments
3. Test with sample data
4. Check the Flask error messages in the console
