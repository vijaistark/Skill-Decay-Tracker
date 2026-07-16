from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import Skill, PracticeLog
from .forms import RegisterForm, SkillForm, PracticeLogForm
from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Helper to mimic Flask session user retrieval
def get_current_user(request):
    return request.user if request.user.is_authenticated else None


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
                user.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
            except Exception:
                messages.error(request, 'An error occurred. Please try again.')
                return redirect('register')
        else:
            for err in form.non_field_errors():
                messages.error(request, err)
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Username and password are required')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('login')


@login_required
def skills(request):
    user = get_current_user(request)
    skills = Skill.objects.filter(user_id=user.id)
    for skill in skills:
        skill.strength = skill.get_strength_score()
        skill.warning = skill.should_show_warning()
    return render(request, 'skills.html', {'skills': skills})


@login_required
def add_skill(request):
    user = get_current_user(request)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            existing_skill = Skill.objects.filter(user_id=user.id, skill_name=form.cleaned_data['skill_name']).first()
            if existing_skill:
                messages.warning(request, 'You already have this skill in your list')
                return redirect('skills')
            skill = form.save(commit=False)
            skill.user = user
            skill.save()
            messages.success(request, f'Skill "{skill.skill_name}" added successfully!')
            return redirect('skills')
        else:
            messages.error(request, 'Please correct the errors below')
            return render(request, 'add_skill.html', {'form': form})
    else:
        form = SkillForm()
    return render(request, 'add_skill.html', {'form': form})


@login_required
def edit_skill(request, skill_id):
    user = get_current_user(request)
    skill = get_object_or_404(Skill, id=skill_id)
    if skill.user_id != user.id:
        messages.error(request, 'You do not have permission to edit this skill')
        return redirect('skills')
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, f'Skill "{skill.skill_name}" updated successfully!')
            return redirect('skills')
        else:
            messages.error(request, 'Please correct the errors below')
            return render(request, 'edit_skill.html', {'form': form, 'skill': skill})
    else:
        form = SkillForm(instance=skill)
    return render(request, 'edit_skill.html', {'form': form, 'skill': skill})


@login_required
def delete_skill(request, skill_id):
    user = get_current_user(request)
    skill = get_object_or_404(Skill, id=skill_id)
    if skill.user_id != user.id:
        messages.error(request, 'You do not have permission to delete this skill')
        return redirect('skills')
    try:
        skill_name = skill.skill_name
        skill.delete()
        messages.success(request, f'Skill "{skill_name}" deleted successfully!')
    except Exception:
        messages.error(request, 'An error occurred while deleting the skill')
    return redirect('skills')


@login_required
def log_practice(request, skill_id):
    user = get_current_user(request)
    skill = get_object_or_404(Skill, id=skill_id)
    if skill.user_id != user.id:
        messages.error(request, 'You do not have permission to log practice for this skill')
        return redirect('skills')
    if request.method == 'POST':
        form = PracticeLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.skill = skill
            log.save()
            messages.success(request, 'Practice session logged successfully!')
            return redirect('skill_detail', skill_id=skill_id)
        else:
            messages.error(request, 'Please correct the errors below')
            return render(request, 'log_practice.html', {'skill': skill, 'form': form})
    else:
        form = PracticeLogForm()
    return render(request, 'log_practice.html', {'skill': skill, 'form': form})


@login_required
def skill_detail(request, skill_id):
    user = get_current_user(request)
    skill = get_object_or_404(Skill, id=skill_id)
    if skill.user_id != user.id:
        messages.error(request, 'You do not have permission to view this skill')
        return redirect('skills')
    practice_logs = PracticeLog.objects.filter(skill_id=skill_id).order_by('-practice_date')
    total_hours = sum(log.hours_practiced for log in practice_logs)
    strength = skill.get_strength_score()
    days_since = skill.get_days_since_practice()
    warning = skill.should_show_warning()
    return render(request, 'skill_detail.html', {
        'skill': skill,
        'practice_logs': practice_logs,
        'total_hours': total_hours,
        'strength': strength,
        'days_since': days_since,
        'warning': warning
    })


@login_required
def dashboard(request):
    user = get_current_user(request)
    skills = Skill.objects.filter(user_id=user.id)
    if not skills:
        total_skills = 0
        strongest_skill = None
        weakest_skill = None
        average_strength = 0
        recent_logs = []
        skills_with_warnings = []
    else:
        skill_data = []
        for skill in skills:
            strength = skill.get_strength_score()
            warning = skill.should_show_warning()
            skill_data.append({'skill': skill, 'strength': strength, 'warning': warning})
        total_skills = len(skills)
        strongest_skill = max(skill_data, key=lambda x: x['strength'])
        weakest_skill = min(skill_data, key=lambda x: x['strength'])
        average_strength = sum(s['strength'] for s in skill_data) / total_skills if total_skills > 0 else 0
        recent_logs = PracticeLog.objects.filter(skill__user_id=user.id).order_by('-practice_date')[:10]
        skills_with_warnings = [s for s in skill_data if s['warning']]
    return render(request, 'dashboard.html', {
        'user': user,
        'total_skills': total_skills,
        'strongest_skill': strongest_skill,
        'weakest_skill': weakest_skill,
        'average_strength': average_strength,
        'recent_logs': recent_logs,
        'skills_with_warnings': skills_with_warnings,
        'skills': skills
    })
