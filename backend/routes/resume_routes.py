"""
Resume-Based Interview Routes
API endpoints for resume upload and analysis
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from utils.resume_parser import ResumeParser
from utils.question_generator import QuestionGenerator
from utils.answer_evaluator import AnswerEvaluator
from models.database import create_session, save_resume_analysis, save_qa_record

bp = Blueprint('resume', __name__, url_prefix='/api/resume')

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Parse resume
        parsed_data = ResumeParser.parse_resume(filepath)
        
        if 'error' in parsed_data:
            return jsonify(parsed_data), 500
        
        # Create session
        session_id = create_session('resume')
        
        # Save resume analysis
        save_resume_analysis(
            session_id,
            filepath,
            parsed_data['skills'],
            parsed_data['education'],
            parsed_data['projects']
        )
        
        # Generate personalized questions
        questions_data = QuestionGenerator.generate_resume_questions(
            parsed_data['skills'],
            parsed_data['education'],
            parsed_data['projects']
        )
        
        return jsonify({
            'session_id': session_id,
            'parsed_data': parsed_data,
            'questions': questions_data['questions'],
            'total_questions': questions_data['total']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/evaluate', methods=['POST'])
def evaluate_resume_answer():
    """Evaluate answer for resume-based question"""
    try:
        data = request.json
        session_id = data.get('session_id')
        question = data.get('question')
        answer = data.get('answer')
        question_type = data.get('question_type', 'general')
        resume_keywords = data.get('resume_keywords', [])
        
        if not all([session_id, question, answer]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Evaluate answer
        result = AnswerEvaluator.evaluate_resume_answer(
            question, 
            answer, 
            question_type, 
            resume_keywords
        )
        
        # Save to database
        save_qa_record(
            session_id,
            question,
            answer,
            result['score'],
            result['feedback'],
            result['matched_keywords']
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500