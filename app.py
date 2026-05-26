from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Skill, PracticeLog
from datetime import datetime, timedelta
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skill_decay_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Initialize database
db.init_app(app)

# Create app context and initialize database
with app.app_context():
    db.create_all()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def login_required(f):
    """Decorator to check if user is logged in"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


def get_current_user():
    """Get the currently logged in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password or not confirm_password:
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 4:
            flash('Password must be at least 4 characters long', 'danger')
            return redirect(url_for('register'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ============================================================================
# SKILL MANAGEMENT ROUTES
# ============================================================================

@app.route('/skills')
@login_required
def skills():
    """View all skills for the logged in user"""
    user = get_current_user()
    skills = Skill.query.filter_by(user_id=user.id).all()
    
    # Add strength score and warning status to each skill
    for skill in skills:
        skill.strength = skill.get_strength_score()
        skill.warning = skill.should_show_warning()
    
    return render_template('skills.html', skills=skills)


@app.route('/skill/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    """Add a new skill"""
    if request.method == 'POST':
        skill_name = request.form.get('skill_name')
        level = request.form.get('level', 'Beginner')
        learning_date_str = request.form.get('learning_date')
        
        # Validation
        if not skill_name:
            flash('Skill name is required', 'danger')
            return redirect(url_for('add_skill'))
        
        if not learning_date_str:
            flash('Learning date is required', 'danger')
            return redirect(url_for('add_skill'))
        
        # Check if skill already exists for this user
        user = get_current_user()
        existing_skill = Skill.query.filter_by(
            user_id=user.id,
            skill_name=skill_name
        ).first()
        
        if existing_skill:
            flash('You already have this skill in your list', 'warning')
            return redirect(url_for('skills'))
        
        try:
            learning_date = datetime.strptime(learning_date_str, '%Y-%m-%d')
            
            skill = Skill(
                user_id=user.id,
                skill_name=skill_name,
                level=level,
                learning_date=learning_date
            )
            db.session.add(skill)
            db.session.commit()
            flash(f'Skill "{skill_name}" added successfully!', 'success')
            return redirect(url_for('skills'))
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(url_for('add_skill'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the skill', 'danger')
            return redirect(url_for('add_skill'))
    
    return render_template('add_skill.html')


@app.route('/skill/<int:skill_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    """Edit an existing skill"""
    user = get_current_user()
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if skill belongs to current user
    if skill.user_id != user.id:
        flash('You do not have permission to edit this skill', 'danger')
        return redirect(url_for('skills'))
    
    if request.method == 'POST':
        skill_name = request.form.get('skill_name')
        level = request.form.get('level')
        
        if not skill_name:
            flash('Skill name is required', 'danger')
            return redirect(url_for('edit_skill', skill_id=skill_id))
        
        # Check if another skill with the same name exists
        existing_skill = Skill.query.filter_by(
            user_id=user.id,
            skill_name=skill_name
        ).filter(Skill.id != skill_id).first()
        
        if existing_skill:
            flash('You already have another skill with this name', 'warning')
            return redirect(url_for('edit_skill', skill_id=skill_id))
        
        try:
            skill.skill_name = skill_name
            skill.level = level
            db.session.commit()
            flash(f'Skill "{skill_name}" updated successfully!', 'success')
            return redirect(url_for('skills'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the skill', 'danger')
            return redirect(url_for('edit_skill', skill_id=skill_id))
    
    return render_template('edit_skill.html', skill=skill)


@app.route('/skill/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    """Delete a skill"""
    user = get_current_user()
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if skill belongs to current user
    if skill.user_id != user.id:
        flash('You do not have permission to delete this skill', 'danger')
        return redirect(url_for('skills'))
    
    try:
        skill_name = skill.skill_name
        db.session.delete(skill)
        db.session.commit()
        flash(f'Skill "{skill_name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the skill', 'danger')
    
    return redirect(url_for('skills'))


# ============================================================================
# PRACTICE LOGGING ROUTES
# ============================================================================

@app.route('/skill/<int:skill_id>/log', methods=['GET', 'POST'])
@login_required
def log_practice(skill_id):
    """Log a practice session for a skill"""
    user = get_current_user()
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if skill belongs to current user
    if skill.user_id != user.id:
        flash('You do not have permission to log practice for this skill', 'danger')
        return redirect(url_for('skills'))
    
    if request.method == 'POST':
        hours_str = request.form.get('hours_practiced')
        activity_description = request.form.get('activity_description')
        practice_date_str = request.form.get('practice_date')
        
        # Validation
        if not hours_str:
            flash('Hours practiced is required', 'danger')
            return redirect(url_for('log_practice', skill_id=skill_id))
        
        if not practice_date_str:
            flash('Practice date is required', 'danger')
            return redirect(url_for('log_practice', skill_id=skill_id))
        
        try:
            hours = float(hours_str)
            if hours <= 0:
                flash('Hours practiced must be greater than 0', 'danger')
                return redirect(url_for('log_practice', skill_id=skill_id))
            
            practice_date = datetime.strptime(practice_date_str, '%Y-%m-%d')
            
            # Don't allow future dates
            if practice_date > datetime.utcnow():
                flash('Practice date cannot be in the future', 'danger')
                return redirect(url_for('log_practice', skill_id=skill_id))
            
            log = PracticeLog(
                skill_id=skill_id,
                hours_practiced=hours,
                activity_description=activity_description or '',
                practice_date=practice_date
            )
            db.session.add(log)
            db.session.commit()
            flash(f'Practice session logged successfully!', 'success')
            return redirect(url_for('skill_detail', skill_id=skill_id))
        except ValueError:
            flash('Invalid input. Please check your entries.', 'danger')
            return redirect(url_for('log_practice', skill_id=skill_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while logging practice', 'danger')
            return redirect(url_for('log_practice', skill_id=skill_id))
    
    return render_template('log_practice.html', skill=skill)


@app.route('/skill/<int:skill_id>/detail')
@login_required
def skill_detail(skill_id):
    """View details and practice logs for a specific skill"""
    user = get_current_user()
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if skill belongs to current user
    if skill.user_id != user.id:
        flash('You do not have permission to view this skill', 'danger')
        return redirect(url_for('skills'))
    
    # Get practice logs for this skill, sorted by date (newest first)
    practice_logs = PracticeLog.query.filter_by(skill_id=skill_id).order_by(
        PracticeLog.practice_date.desc()
    ).all()
    
    # Calculate metrics
    total_hours = sum(log.hours_practiced for log in practice_logs)
    strength = skill.get_strength_score()
    days_since = skill.get_days_since_practice()
    warning = skill.should_show_warning()
    
    return render_template('skill_detail.html',
                          skill=skill,
                          practice_logs=practice_logs,
                          total_hours=total_hours,
                          strength=strength,
                          days_since=days_since,
                          warning=warning)


# ============================================================================
# DASHBOARD ROUTE
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing overview and analytics"""
    user = get_current_user()
    
    # Get all skills for the user
    skills = Skill.query.filter_by(user_id=user.id).all()
    
    if not skills:
        total_skills = 0
        strongest_skill = None
        weakest_skill = None
        average_strength = 0
        recent_logs = []
        skills_with_warnings = []
    else:
        # Calculate metrics for each skill
        skill_data = []
        for skill in skills:
            strength = skill.get_strength_score()
            warning = skill.should_show_warning()
            skill_data.append({
                'skill': skill,
                'strength': strength,
                'warning': warning
            })
        
        total_skills = len(skills)
        strongest_skill = max(skill_data, key=lambda x: x['strength'])
        weakest_skill = min(skill_data, key=lambda x: x['strength'])
        average_strength = sum(s['strength'] for s in skill_data) / total_skills if total_skills > 0 else 0
        
        # Get recent practice logs (last 10)
        recent_logs = PracticeLog.query.join(Skill).filter(
            Skill.user_id == user.id
        ).order_by(PracticeLog.practice_date.desc()).limit(10).all()
        
        # Get skills with warnings
        skills_with_warnings = [s for s in skill_data if s['warning']]
    
    return render_template('dashboard.html',
                          user=user,
                          total_skills=total_skills,
                          strongest_skill=strongest_skill,
                          weakest_skill=weakest_skill,
                          average_strength=average_strength,
                          recent_logs=recent_logs,
                          skills_with_warnings=skills_with_warnings,
                          skills=skills)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True)
