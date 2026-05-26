from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user account information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to skills
    skills = db.relationship('Skill', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hashed password"""
        return check_password_hash(self.password, password)


class Skill(db.Model):
    """Skill model for storing user skills and their current level"""
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(20), default='Beginner')  # Beginner, Intermediate, Advanced
    learning_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to practice logs
    practice_logs = db.relationship('PracticeLog', backref='skill', lazy=True, cascade='all, delete-orphan')
    
    def get_strength_score(self):
        """
        Calculate skill strength based on practice activity.
        
        Formula:
        - Start with base score of 100
        - Lose 1 point for each day of inactivity
        - Gain points from recent practice sessions
        - Min score: 0, Max score: 100
        """
        base_score = 100
        
        # Get the last practice log
        last_practice = PracticeLog.query.filter_by(skill_id=self.id).order_by(
            PracticeLog.practice_date.desc()
        ).first()
        
        if not last_practice:
            # No practice logs yet - calculate from learning date
            days_inactive = (datetime.utcnow() - self.learning_date).days
            strength = base_score - days_inactive
        else:
            # Calculate based on last practice
            days_since_practice = (datetime.utcnow() - last_practice.practice_date).days
            inactivity_penalty = days_since_practice * 1  # lose 1 point per day
            
            # Add bonus from recent practices (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_logs = PracticeLog.query.filter(
                PracticeLog.skill_id == self.id,
                PracticeLog.practice_date >= thirty_days_ago
            ).all()
            
            practice_bonus = sum(log.hours_practiced for log in recent_logs) * 2  # 2 points per hour
            
            strength = base_score - inactivity_penalty + practice_bonus
        
        # Ensure score is between 0 and 100
        return max(0, min(100, strength))
    
    def get_days_since_practice(self):
        """Get the number of days since the last practice"""
        last_practice = PracticeLog.query.filter_by(skill_id=self.id).order_by(
            PracticeLog.practice_date.desc()
        ).first()
        
        if not last_practice:
            return (datetime.utcnow() - self.learning_date).days
        
        return (datetime.utcnow() - last_practice.practice_date).days
    
    def should_show_warning(self):
        """Return True if skill should show a warning (no practice in 7+ days or strength below 40)"""
        days_inactive = self.get_days_since_practice()
        strength = self.get_strength_score()
        
        return days_inactive >= 7 or strength < 40


class PracticeLog(db.Model):
    """Practice log model for tracking practice sessions"""
    __tablename__ = 'practice_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    hours_practiced = db.Column(db.Float, nullable=False)
    activity_description = db.Column(db.String(500), nullable=True)
    practice_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
