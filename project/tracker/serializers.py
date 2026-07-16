from rest_framework import serializers
from .models import Skill, PracticeLog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class PracticeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeLog
        fields = ('id', 'skill', 'hours_practiced', 'activity_description', 'practice_date', 'created_at')


class SkillSerializer(serializers.ModelSerializer):
    practice_logs = PracticeLogSerializer(many=True, read_only=True)

    class Meta:
        model = Skill
        fields = ('id', 'user', 'skill_name', 'level', 'learning_date', 'created_at', 'practice_logs')
