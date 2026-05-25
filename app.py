import os
from flask import Flask, render_template
from database import init_db

def create_app():
    app = Flask(__name__)
    # session secret and database configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        db_path = os.path.join(app.instance_path, 'db.sqlite3')
        os.makedirs(app.instance_path, exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    # register blueprints
    from routes.auth import auth_bp
    from routes.interviews import interview_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(interview_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
