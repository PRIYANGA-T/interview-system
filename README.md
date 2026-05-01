<<<<<<< HEAD
# Generative AI Powered Interview Evaluation System

A complete, production-ready interview evaluation system using Generative AI, Natural Language Processing, and Computer Vision for comprehensive candidate assessment.

## 🎯 Features

### Module 1: Domain-Based Interview Evaluation
- **6 Technical Domains**: Frontend, Backend, Python, AI/ML, DBMS, Cloud
- **AI Question Generation**: Dynamic questions based on domain
- **Intelligent Evaluation**: 
  - Keyword matching
  - Semantic similarity analysis
  - Relevance scoring
- **Detailed Feedback**:
  - Score out of 10
  - Strengths identification
  - Weak areas analysis
  - Personalized improvement suggestions

### Module 2: Resume-Based Interview Evaluation
- **PDF Resume Upload**: Drag-and-drop or browse
- **Intelligent Parsing**:
  - Skills extraction
  - Education details
  - Projects identification
- **Personalized Questions**: Based on resume content
- **Resume Alignment Score**: Measures answer relevance to resume
- **Comprehensive Feedback**: Targeted suggestions based on profile

### Module 3: Behavioral & Emotion Analysis
- **Webcam Integration**: Real-time video capture
- **5 Behavioral Questions**:
  1. Introduce yourself
  2. Why should I hire you?
  3. Where do you see yourself after 5 years?
  4. Why did you choose this company?
  5. Why did you choose this degree?
- **Emotion Detection**: Uses OpenCV for facial analysis
  - Confident
  - Neutral
  - Nervous
  - Anxious
- **Comprehensive Scoring**:
  - Communication score
  - Confidence score
  - Emotion timeline
  - Behavioral suggestions

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python, Flask
- **AI/NLP**: Custom generative AI logic with semantic analysis
- **Emotion Analysis**: OpenCV with Haar Cascades (no paid APIs)
- **Database**: SQLite
- **Architecture**: REST API

## 📁 Project Structure

```
interview-system/
├── backend/
│   ├── app.py                          # Main Flask application
│   ├── models/
│   │   └── database.py                 # Database models and operations
│   ├── routes/
│   │   ├── question_routes.py          # Question generation endpoints
│   │   ├── evaluation_routes.py        # Answer evaluation endpoints
│   │   ├── resume_routes.py            # Resume processing endpoints
│   │   └── emotion_routes.py           # Emotion detection endpoints
│   └── utils/
│       ├── question_generator.py       # AI question generation
│       ├── answer_evaluator.py         # Answer evaluation engine
│       ├── resume_parser.py            # PDF resume parser
│       └── emotion_detector.py         # Emotion detection with OpenCV
├── templates/
│   ├── index.html                      # Main landing page
│   ├── domain_interview.html           # Domain interview interface
│   ├── resume_interview.html           # Resume interview interface
│   └── behavioral_interview.html       # Behavioral interview interface
├── static/
│   ├── css/
│   │   └── style.css                   # Main stylesheet
│   └── js/
│       ├── domain-interview.js         # Domain interview logic
│       ├── resume-interview.js         # Resume interview logic
│       └── behavioral-interview.js     # Behavioral interview logic
├── database/
│   └── interview_system.db             # SQLite database (auto-created)
├── uploads/                            # Resume uploads (auto-created)
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser with webcam support
- Webcam (for behavioral interview module)

### Step 1: Clone/Download the Project

```bash
cd interview-system
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues with OpenCV on Linux, you may need to install additional dependencies:
```bash
sudo apt-get install python3-opencv
# OR
pip install opencv-python-headless
```

### Step 4: Run the Application

```bash
cd backend
python app.py
```

You should see output like:
```
============================================================
🚀 Interview Evaluation System Starting...
============================================================
📍 Main Page: http://localhost:5000
📍 Domain Interview: http://localhost:5000/domain-interview
📍 Resume Interview: http://localhost:5000/resume-interview
📍 Behavioral Interview: http://localhost:5000/behavioral-interview
============================================================
✅ Database initialized successfully
 * Running on http://0.0.0.0:5000
```

### Step 5: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Domain-Based Interview

1. Click "Start Domain Interview" on the home page
2. Select your domain (Frontend, Backend, Python, AI/ML, DBMS, or Cloud)
3. Answer 5 AI-generated questions
4. Get instant feedback with:
   - Score out of 10
   - Matched keywords
   - Strengths and weaknesses
   - Improvement suggestions
5. View final results with comprehensive analysis

### Resume-Based Interview

1. Click "Start Resume Interview" on the home page
2. Upload your resume (PDF format, max 5MB)
3. Review extracted information:
   - Skills
   - Education
   - Projects
4. Answer personalized questions
5. Get feedback with:
   - Overall score
   - Resume alignment percentage
   - Targeted suggestions

### Behavioral Interview with Emotion Analysis

1. Click "Start Behavioral Interview" on the home page
2. Allow camera access when prompted
3. Answer 5 behavioral questions while being recorded
4. System analyzes:
   - Your facial expressions in real-time
   - Confidence levels
   - Communication quality
5. Get comprehensive report:
   - Overall score
   - Communication score
   - Confidence score
   - Emotion timeline
   - Dominant emotion
   - Personalized behavioral suggestions

## 🔧 Configuration

### Database
The system uses SQLite by default. Database file is created automatically at:
```
database/interview_system.db
```

### File Upload
Resume uploads are stored in:
```
uploads/
```
Maximum file size: 16MB (configurable in `app.py`)

### Port Configuration
Default port is 5000. To change, modify in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

## 🎨 Features Breakdown

### AI Question Generation
- Domain-specific question banks
- Difficulty levels (Easy, Medium, Hard)
- Keywords for evaluation
- Resume-based personalization

### Answer Evaluation
- Keyword matching algorithm
- Semantic similarity using cosine similarity
- Length-based scoring
- Weighted scoring based on difficulty
- Comprehensive feedback generation

### Resume Parsing
- PDF text extraction using PyPDF2
- Skill keyword detection (50+ technologies)
- Education information extraction
- Project identification
- Intelligent keyword extraction for evaluation

### Emotion Detection
- OpenCV Haar Cascade for face detection
- Facial feature analysis
- Emotion classification (Confident, Neutral, Nervous, Anxious)
- Real-time confidence scoring
- Emotion timeline tracking
- Consistency analysis

## 📊 Database Schema

### interview_sessions
- id, session_type, domain, created_at, total_score, status

### qa_records
- id, session_id, question, answer, score, feedback, keywords_matched, created_at

### resume_analysis
- id, session_id, resume_path, extracted_skills, extracted_education, extracted_projects, created_at

### behavioral_analysis
- id, session_id, question, answer, emotion_detected, confidence_score, communication_score, timestamp

### emotion_timeline
- id, session_id, emotion, confidence, timestamp

## 🧪 Sample Test Data

### Testing Domain Interview
Try these sample answers for better scores:

**Frontend - "Explain var, let, and const"**
```
var is function-scoped and can be hoisted, while let and const are block-scoped. 
const cannot be reassigned after declaration, but let can be. var allows 
redeclaration in the same scope, which can lead to bugs.
```

**Python - "Explain decorators"**
```
Decorators are a design pattern that allows you to modify the behavior of a 
function or class. They use the @ syntax and are essentially wrapper functions 
that take another function as an argument and extend its behavior without 
modifying it.
```

### Testing Resume Upload
Create a simple PDF resume with:
- Skills: Python, JavaScript, React, Flask, Machine Learning
- Education: Bachelor's in Computer Science
- Projects: E-commerce Platform, Chatbot Application

## 🐛 Troubleshooting

### Camera Not Working
- Ensure browser has camera permissions
- Check if camera is being used by another application
- Try a different browser (Chrome/Firefox recommended)
- For HTTPS: Camera requires secure connection

### Resume Upload Failing
- Ensure file is PDF format
- Check file size (should be under 5MB)
- Verify file is not corrupted
- Check uploads folder has write permissions

### Emotion Detection Not Working
- Ensure good lighting conditions
- Face should be clearly visible
- Camera should be at eye level
- Avoid extreme angles

### Database Errors
```bash
# Delete existing database and restart
rm database/interview_system.db
python backend/app.py
```

## 🔒 Security Considerations

- File upload validation (PDF only, size limits)
- SQL injection prevention (parameterized queries)
- XSS prevention (proper input sanitization)
- CORS configured for localhost
- Session management for multi-user support

## 🚀 Production Deployment

For production deployment:

1. **Disable Debug Mode**:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

2. **Use Production Server** (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Set up HTTPS** (required for webcam on production)

4. **Configure Database** for production (PostgreSQL recommended)

5. **Set Environment Variables**:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
```

## 📝 API Endpoints

### Questions
- `POST /api/questions/domain` - Generate domain questions
- `GET /api/questions/behavioral` - Get behavioral questions

### Evaluation
- `POST /api/evaluate/answer` - Evaluate single answer
- `POST /api/evaluate/session/<id>/complete` - Complete session
- `GET /api/evaluate/session/<id>/results` - Get session results

### Resume
- `POST /api/resume/upload` - Upload and parse resume
- `POST /api/resume/evaluate` - Evaluate resume-based answer

### Emotion
- `POST /api/emotion/analyze` - Analyze emotion from image
- `POST /api/emotion/behavioral/submit` - Submit behavioral answer
- `POST /api/emotion/behavioral/complete/<id>` - Complete behavioral interview

## 🎓 Project Information

**Type**: MCA Final Year Project  
**Domain**: Artificial Intelligence, Natural Language Processing, Computer Vision  
**Complexity**: Advanced  
**Development Time**: Comprehensive full-stack application

## 📄 License

This project is created for educational purposes as an MCA final year project.

## 👨‍💻 Author

MCA Final Year Project  
Generative AI Powered Interview Evaluation System

## 🙏 Acknowledgments

- OpenCV for computer vision capabilities
- Flask framework for robust backend
- PyPDF2 for PDF processing
- SQLite for lightweight database

---

**Note**: This is a complete, runnable project with all modules integrated. Follow the setup instructions carefully for the best experience.
=======
# interview-system
>>>>>>> 828aa71ce4fea6348d2719fe6d9aff7ac159168c
