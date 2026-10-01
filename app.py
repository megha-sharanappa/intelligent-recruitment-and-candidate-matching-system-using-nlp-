import os
from pathlib import Path
from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure Upload Folder Exists
    upload_folder = Path(app.config['UPLOAD_FOLDER'])
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from routes import (
        auth_bp,
        candidate_bp,
        recruiter_bp,
        jobs_bp,
        applications_bp,
        resume_bp,
        profiles_bp,
        api_bp
    )
    app.register_blueprint(auth_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(api_bp)

    # Home Route
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            if current_user.is_candidate:
                return redirect(url_for('candidate.dashboard'))
            elif current_user.is_recruiter:
                return redirect(url_for('recruiter.dashboard'))
        from models import Job
        featured_jobs = Job.query.filter_by(is_published=True, is_closed=False).order_by(Job.created_at.desc()).limit(6).all()
        return render_template('index.html', featured_jobs=featured_jobs)

    # Custom Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Initialize Database Tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            # Fallback to SQLite if MySQL connection failed
            print(f"Primary database connection notice: {e}. Falling back to SQLite.")
            sqlite_uri = f"sqlite:///{Path(__file__).resolve().parent / 'recruitment.db'}"
            app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
            db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    print(f"Starting Intelligent Recruitment and Candidate Matching System on http://127.0.0.1:{port}")
    app.run(host=host, port=port, debug=True)
