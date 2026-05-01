"""
Generative AI Powered Interview Evaluation System
Main Flask Application
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes import question_routes, evaluation_routes, resume_routes, emotion_routes
from models.database import init_db

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Create uploads directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(question_routes.bp)
app.register_blueprint(evaluation_routes.bp)
app.register_blueprint(resume_routes.bp)
app.register_blueprint(emotion_routes.bp)

@app.route('/')
def index():
    """Serve main application page"""
    return render_template('index.html')

@app.route('/domain-interview')
def domain_interview():
    """Serve domain-based interview page"""
    return render_template('domain_interview.html')

@app.route('/resume-interview')
def resume_interview():
    """Serve resume-based interview page"""
    return render_template('resume_interview.html')

@app.route('/behavioral-interview')
def behavioral_interview():
    """Serve behavioral interview page"""
    return render_template('behavioral_interview.html')


@app.route('/python-mcq')
def python_mcq():
    """Serve Python MCQ assessment page"""
    return render_template('python_mcq.html')


@app.route('/aptitude-mcq')
def aptitude_mcq():
    """Serve aptitude MCQ assessment page"""
    return render_template('aptitude_mcq.html')


@app.route('/dashboard')
def dashboard():
    """Serve interview analytics dashboard"""
    return render_template('dashboard.html')

@app.route('/results/<int:session_id>')
def results(session_id):
    """Serve results page"""
    return render_template('results.html', session_id=session_id)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Interview System is running"})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Interview Evaluation System Starting...")
    print("=" * 60)
    print("📍 Main Page: http://localhost:5000")
    print("📍 Domain Interview: http://localhost:5000/domain-interview")
    print("📍 Resume Interview: http://localhost:5000/resume-interview")
    print("📍 Behavioral Interview: http://localhost:5000/behavioral-interview")
    print("📍 Python MCQ: http://localhost:5000/python-mcq")
    print("📍 Aptitude MCQ: http://localhost:5000/aptitude-mcq")
    print("📍 Dashboard: http://localhost:5000/dashboard")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)