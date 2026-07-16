from django.db import models
from django.conf import settings
from django.utils import timezone


class Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, default='Beginner')
    learning_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.skill_name

    def get_strength_score(self):
        from .models import PracticeLog
        from datetime import timedelta
        base_score = 100
        last_practice = PracticeLog.objects.filter(skill_id=self.id).order_by('-practice_date').first()
        if not last_practice:
            days_inactive = (timezone.now() - self.learning_date).days
            strength = base_score - days_inactive
        else:
            days_since_practice = (timezone.now() - last_practice.practice_date).days
            inactivity_penalty = days_since_practice * 1
            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_logs = PracticeLog.objects.filter(skill_id=self.id, practice_date__gte=thirty_days_ago)
            practice_bonus = sum(log.hours_practiced for log in recent_logs) * 2
            strength = base_score - inactivity_penalty + practice_bonus
        return max(0, min(100, strength))

    def get_days_since_practice(self):
        from .models import PracticeLog
        last_practice = PracticeLog.objects.filter(skill_id=self.id).order_by('-practice_date').first()
        if not last_practice:
            return (timezone.now() - self.learning_date).days
        return (timezone.now() - last_practice.practice_date).days

    def should_show_warning(self):
        days_inactive = self.get_days_since_practice()
        strength = self.get_strength_score()
        return days_inactive >= 7 or strength < 40


class PracticeLog(models.Model):
    skill = models.ForeignKey(Skill, related_name='practice_logs', on_delete=models.CASCADE)
    hours_practiced = models.FloatField()
    activity_description = models.CharField(max_length=500, blank=True, null=True)
    practice_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.skill.skill_name} - {self.practice_date.date()}"
