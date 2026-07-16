# Skill Decay Tracker - Django Migration

This repository contains a Django migration of the original Flask `Skill-Decay-Tracker` application. The goal is to preserve the UI and behavior while moving the backend to Django + Django REST Framework.

Quick start

1. Create and activate a virtualenv

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

5. Run the dev server

```bash
python manage.py runserver
```

APIs

- `/api/skills/` - CRUD for skills
- `/api/logs/` - CRUD for practice logs
- `/api/dashboard/?user=<id>` - dashboard stats

Notes

- This migration preserves templates and static CSS/JS from the Flask app.
- Authentication currently uses a simple session-based approach to match the Flask behavior. You can migrate to Django's `auth` easily by wiring `django.contrib.auth` models and views.
