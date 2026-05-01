# 🚀 QUICK START GUIDE

## Installation (5 Minutes)

### Windows:
```cmd
1. Extract the project folder
2. Open Command Prompt in project folder
3. Double-click start.bat
```

### Linux/Mac:
```bash
1. Extract the project folder
2. Open Terminal in project folder
3. chmod +x start.sh
4. ./start.sh
```

### Manual Setup:
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
cd backend
python app.py
```

## First Run

1. **Open Browser**: http://localhost:5000

2. **Test Domain Interview**:
   - Click "Start Domain Interview"
   - Select "Python" domain
   - Answer: "Python is a high-level programming language with simple syntax and powerful libraries for web development, data science, and automation"
   - Expected score: 7-9/10

3. **Test Resume Interview**:
   - Click "Start Resume Interview"  
   - Upload sample PDF resume (or create one with skills like Python, React, etc.)
   - Answer personalized questions

4. **Test Behavioral Interview**:
   - Click "Start Behavioral Interview"
   - Allow camera access
   - Answer behavioral questions
   - Watch emotion detection in action

## Project Files

📦 **interview-system/**
├── 📄 **README.md** - Complete documentation
├── 📄 **ARCHITECTURE.md** - System architecture
├── 📄 **SAMPLE_OUTPUTS.md** - Expected outputs & test cases
├── 📄 **requirements.txt** - Python dependencies
├── 📄 **test_setup.py** - Verify installation
├── 📄 **start.sh** - Linux/Mac launcher
├── 📄 **start.bat** - Windows launcher
│
├── 📁 **backend/** - Flask application
│   ├── **app.py** - Main application
│   ├── 📁 **models/** - Database layer
│   ├── 📁 **routes/** - API endpoints  
│   └── 📁 **utils/** - Core logic
│
├── 📁 **templates/** - HTML pages
│   ├── index.html
│   ├── domain_interview.html
│   ├── resume_interview.html
│   └── behavioral_interview.html
│
└── 📁 **static/** - CSS & JavaScript
    ├── 📁 **css/** - Stylesheets
    └── 📁 **js/** - Frontend logic

## Key Features

✅ **3 Interview Modules**
✅ **AI Question Generation**
✅ **Intelligent Answer Evaluation**  
✅ **Resume Parsing (PDF)**
✅ **Webcam Emotion Detection**
✅ **Real-time Scoring**
✅ **Comprehensive Feedback**
✅ **SQLite Database**
✅ **No External APIs Required**
✅ **Production-Ready Code**

## Verification

Run test script:
```bash
python test_setup.py
```

Should show:
```
✅ Python 3.x
✅ All modules installed
✅ Project structure verified
✅ Database initialized
✅ Question generation working
✅ Answer evaluation working
✅ Emotion detector ready
✅ Flask app configured
```

## Troubleshooting

**Import Errors?**
```bash
pip install -r requirements.txt
```

**Camera Not Working?**
- Allow browser camera permissions
- Use Chrome or Firefox
- Check camera is not used by other app

**Port 5000 Busy?**
Edit `backend/app.py`, change port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## Next Steps

1. ✅ Install and run (5 min)
2. ✅ Test all 3 modules (10 min)
3. ✅ Read ARCHITECTURE.md for details
4. ✅ Check SAMPLE_OUTPUTS.md for examples
5. ✅ Customize question banks
6. ✅ Add your own domains
7. ✅ Deploy to production

## Support

📖 Full Documentation: README.md
🏗️ Architecture: ARCHITECTURE.md
📊 Sample Outputs: SAMPLE_OUTPUTS.md
🧪 Test Script: test_setup.py

---

**READY TO INTERVIEW! 🎯**

Access the system at: **http://localhost:5000**