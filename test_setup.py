#!/usr/bin/env python3
"""
Installation and Setup Verification Script
Tests all components of the Interview Evaluation System
"""

import sys
import os

print("=" * 60)
print("🔍 Interview System - Installation Verification")
print("=" * 60)
print()

# Test 1: Python Version
print("Test 1: Checking Python Version...")
if sys.version_info < (3, 8):
    print("❌ FAILED: Python 3.8+ required")
    print(f"   Current version: {sys.version}")
    sys.exit(1)
else:
    print(f"✅ PASSED: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print()

# Test 2: Import Required Modules
print("Test 2: Checking Required Modules...")
required_modules = {
    'flask': 'Flask',
    'flask_cors': 'Flask-CORS',
    'PyPDF2': 'PyPDF2',
    'cv2': 'OpenCV',
    'numpy': 'NumPy',
    'PIL': 'Pillow'
}

all_passed = True
for module, name in required_modules.items():
    try:
        __import__(module)
        print(f"✅ {name}: Installed")
    except ImportError:
        print(f"❌ {name}: Not installed")
        all_passed = False

if not all_passed:
    print("\n⚠️  Install missing modules with: pip install -r requirements.txt")
    sys.exit(1)
print()

# Test 3: Check Project Structure
print("Test 3: Verifying Project Structure...")
required_dirs = [
    'backend',
    'backend/models',
    'backend/routes',
    'backend/utils',
    'templates',
    'static',
    'static/css',
    'static/js'
]

required_files = [
    'backend/app.py',
    'backend/models/database.py',
    'backend/utils/question_generator.py',
    'backend/utils/answer_evaluator.py',
    'backend/utils/resume_parser.py',
    'backend/utils/emotion_detector.py',
    'templates/index.html',
    'static/css/style.css',
    'requirements.txt',
    'README.md'
]

structure_ok = True

for dir_path in required_dirs:
    if os.path.isdir(dir_path):
        print(f"✅ Directory: {dir_path}")
    else:
        print(f"❌ Missing: {dir_path}")
        structure_ok = False

for file_path in required_files:
    if os.path.isfile(file_path):
        print(f"✅ File: {file_path}")
    else:
        print(f"❌ Missing: {file_path}")
        structure_ok = False

if not structure_ok:
    print("\n⚠️  Project structure incomplete!")
    sys.exit(1)
print()

# Test 4: Database Initialization
print("Test 4: Testing Database Initialization...")
try:
    sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
    from models.database import init_db
    init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"❌ Database initialization failed: {e}")
    sys.exit(1)
print()

# Test 5: Question Generator
print("Test 5: Testing Question Generator...")
try:
    from utils.question_generator import QuestionGenerator
    result = QuestionGenerator.generate_domain_questions('Python', 2)
    if 'questions' in result and len(result['questions']) == 2:
        print("✅ Question generation working")
        print(f"   Sample question: {result['questions'][0]['question'][:60]}...")
    else:
        print("❌ Question generation failed")
        sys.exit(1)
except Exception as e:
    print(f"❌ Question generator error: {e}")
    sys.exit(1)
print()

# Test 6: Answer Evaluator
print("Test 6: Testing Answer Evaluator...")
try:
    from utils.answer_evaluator import AnswerEvaluator
    result = AnswerEvaluator.evaluate_answer(
        "What is Python?",
        "Python is a high-level programming language known for its simplicity and readability",
        ["python", "programming", "language"],
        "easy"
    )
    if 'score' in result and 'feedback' in result:
        print("✅ Answer evaluation working")
        print(f"   Sample score: {result['score']}/10")
    else:
        print("❌ Answer evaluation failed")
        sys.exit(1)
except Exception as e:
    print(f"❌ Answer evaluator error: {e}")
    sys.exit(1)
print()

# Test 7: Emotion Detector
print("Test 7: Testing Emotion Detector...")
try:
    from utils.emotion_detector import EmotionDetector
    detector = EmotionDetector()
    print("✅ Emotion detector initialized")
    print("   OpenCV Haar Cascades loaded successfully")
except Exception as e:
    print(f"❌ Emotion detector error: {e}")
    sys.exit(1)
print()

# Test 8: Flask App Import
print("Test 8: Testing Flask Application...")
try:
    from app import app
    print("✅ Flask app imported successfully")
    print(f"   Secret key configured: {bool(app.config.get('SECRET_KEY'))}")
except Exception as e:
    print(f"❌ Flask app error: {e}")
    sys.exit(1)
print()

# Final Summary
print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print()
print("🎉 Your Interview Evaluation System is ready to run!")
print()
print("To start the application:")
print("  1. cd backend")
print("  2. python app.py")
print()
print("Then open: http://localhost:5000")
print("=" * 60)