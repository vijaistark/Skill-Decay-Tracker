# Interview Failure Pattern Analyzer

Simple student-style Flask app to track mock interviews and detect repeated weak skills.

Quick start:

1. Create virtualenv and install:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. (Optional) Set `DATABASE_URL` env var to a MySQL URI like `mysql+pymysql://user:pass@host/db`.
   By default the app uses `sqlite:///db.sqlite3`.

3. Run:

```bash
python app.py
```

Open http://127.0.0.1:5000

This project is intentionally simple and looks like a student implementation.
