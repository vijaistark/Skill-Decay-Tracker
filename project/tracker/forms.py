from django import forms
from .models import Skill, PracticeLog
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=4)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError('Passwords do not match')
        if User.objects.filter(username=cleaned.get('username')).exists():
            raise forms.ValidationError('Username already exists')
        if User.objects.filter(email=cleaned.get('email')).exists():
            raise forms.ValidationError('Email already exists')
        return cleaned


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('skill_name', 'level', 'learning_date')


class PracticeLogForm(forms.ModelForm):
    class Meta:
        model = PracticeLog
        fields = ('hours_practiced', 'activity_description', 'practice_date')

    def clean_hours_practiced(self):
        hours = self.cleaned_data.get('hours_practiced')
        if hours is None or hours <= 0:
            raise forms.ValidationError('Hours practiced must be greater than 0')
        return hours
