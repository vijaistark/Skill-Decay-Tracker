from django.contrib import admin
from .models import Skill, PracticeLog
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'skill_name', 'user', 'level', 'learning_date', 'created_at')
    search_fields = ('skill_name', 'user__username')
    list_filter = ('level',)


@admin.register(PracticeLog)
class PracticeLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'skill', 'hours_practiced', 'practice_date', 'created_at')
    search_fields = ('skill__skill_name',)
    list_filter = ('practice_date',)
