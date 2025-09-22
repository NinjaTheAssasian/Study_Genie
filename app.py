from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
import os
from datetime import datetime, timedelta
import random
import json
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'studygenie_secret_key_2025'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create directories
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize session history if not exists
def init_history():
    if 'history' not in session:
        session['history'] = {
            'summaries': [],
            'quizzes': [],
            'schedules': []
        }

def create_enhanced_templates():
    # Index template
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudyGenie - AI Study Assistant</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --accent: #06b6d4;
            --dark: #0f172a;
            --light: #f8fafc;
            --gray: #64748b;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, #1e1b4b 100%);
            color: var(--light);
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { text-align: center; margin-bottom: 50px; }
        .logo {
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        nav {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 20px;
            padding: 15px 0;
            margin-bottom: 50px;
        }
        nav ul {
            list-style: none;
            display: flex;
            justify-content: center;
            gap: 30px;
        }
        nav a {
            color: var(--light);
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 25px;
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: all 0.3s;
        }
        nav a:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
        }
        .hero {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 27, 75, 0.9));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 25px;
            padding: 60px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }
        .feature-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 27, 75, 0.8));
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            transition: all 0.3s;
        }
        .feature-card:hover { transform: translateY(-10px); }
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn:hover { transform: translateY(-3px); }
        @media (max-width: 768px) {
            .features { grid-template-columns: 1fr; }
            .hero { padding: 30px; }
        }
        .history-btn {
            background: rgba(6, 182, 212, 0.2);
            border: 1px solid rgba(6, 182, 212, 0.4);
            color: white;
            padding: 8px 16px;
            border-radius: 15px;
            cursor: pointer;
            margin-top: 10px;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">🧞‍♂️ StudyGenie</div>
            <p style="font-size: 1.2rem; color: var(--gray);">Your AI-Powered Study Assistant</p>
        </header>

        <nav>
            <ul>
                <li><a href="/"><i class="fas fa-home"></i> Home</a></li>
                <li><a href="/upload"><i class="fas fa-file-pdf"></i> Summarizer</a></li>
                <li><a href="/quiz"><i class="fas fa-brain"></i> Quiz</a></li>
                <li><a href="/schedule"><i class="fas fa-calendar"></i> Planner</a></li>
                <li><a href="/history"><i class="fas fa-history"></i> History</a></li>
            </ul>
        </nav>

        <main>
            <div class="hero">
                <h2 style="font-size: 2.5rem; text-align: center; margin-bottom: 30px;">Transform Your Study Experience with AI</h2>

                <div class="features">
                    <div class="feature-card">
                        <div style="font-size: 4rem; margin-bottom: 20px;">📄</div>
                        <h3>AI PDF Summarizer</h3>
                        <p>Upload PDFs and get instant summaries</p>
                        <a href="/upload" class="btn">Try Now</a>
                    </div>

                    <div class="feature-card">
                        <div style="font-size: 4rem; margin-bottom: 20px;">🧠</div>
                        <h3>Quiz Generator</h3>
                        <p>Create practice questions from any topic</p>
                        <a href="/quiz" class="btn">Generate</a>
                    </div>

                    <div class="feature-card">
                        <div style="font-size: 4rem; margin-bottom: 20px;">📊</div>
                        <h3>Study Planner</h3>
                        <p>Get personalized study schedules</p>
                        <a href="/schedule" class="btn">Plan</a>
                    </div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>"""

    # Upload template
    upload_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PDF Summarizer - StudyGenie</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --dark: #0f172a; --light: #f8fafc; --gray: #64748b; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, var(--dark) 0%, #1e1b4b 100%); color: var(--light); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        nav { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 20px; padding: 15px; margin-bottom: 30px; text-align: center; }
        nav a { color: var(--light); text-decoration: none; margin: 0 15px; padding: 8px 20px; background: rgba(99, 102, 241, 0.1); border-radius: 20px; }
        .hero { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 25px; padding: 50px; }
        .upload-area { border: 2px dashed rgba(99, 102, 241, 0.5); padding: 40px; text-align: center; border-radius: 20px; margin: 20px 0; }
        .btn { background: linear-gradient(135deg, var(--primary), #8b5cf6); color: white; padding: 15px 40px; border: none; border-radius: 25px; cursor: pointer; font-size: 1.1rem; }
        .summary-box { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 30px; border-radius: 20px; margin: 20px 0; position: relative; }
        .action-buttons { margin-top: 20px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
        .action-btn {
            padding: 10px 20px;
            border-radius: 15px;
            cursor: pointer;
            font-size: 0.9rem;
            border: none;
            transition: all 0.2s;
        }
        .copy-btn { background: rgba(99, 102, 241, 0.2); color: white; }
        .download-btn { background: rgba(16, 185, 129, 0.2); color: white; }
        .copy-btn:hover { background: rgba(99, 102, 241, 0.4); }
        .download-btn:hover { background: rgba(16, 185, 129, 0.4); }
        .error { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 20px; border-radius: 10px; color: #fca5a5; }
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="/"><i class="fas fa-home"></i> Home</a>
            <a href="/upload"><i class="fas fa-file-pdf"></i> Upload</a>
            <a href="/quiz"><i class="fas fa-brain"></i> Quiz</a>
            <a href="/schedule"><i class="fas fa-calendar"></i> Schedule</a>
            <a href="/history"><i class="fas fa-history"></i> History</a>
        </nav>

        <div class="hero">
            <h2 style="text-align: center; margin-bottom: 30px;"><i class="fas fa-magic"></i> AI PDF Summarizer</h2>

            <form method="post" enctype="multipart/form-data">
                <div class="upload-area">
                    <div style="font-size: 4rem; color: var(--primary); margin-bottom: 20px;">
                        <i class="fas fa-cloud-upload-alt"></i>
                    </div>
                    <h3>Upload Your Study Materials</h3>
                    <p>Select a PDF file to summarize (Max: 5MB)</p>
                    <input type="file" name="file" accept=".pdf" required style="width: 100%; padding: 15px; margin: 20px 0; background: rgba(15, 23, 42, 0.8); border: 2px solid rgba(99, 102, 241, 0.3); border-radius: 15px; color: var(--light);">
                </div>
                <button type="submit" class="btn">
                    <i class="fas fa-sparkles"></i> Generate Summary
                </button>
            </form>

            {% if error %}
            <div class="error">
                <strong>Error:</strong> {{ error }}
            </div>
            {% endif %}

            {% if summary %}
            <div class="summary-box">
                <h3 style="margin-bottom: 15px;">📝 Summary Generated Successfully</h3>
                <div id="summaryText">{{ summary }}</div>
                <div class="action-buttons">
                    <button onclick="copySummary()" class="action-btn copy-btn">
                        <i class="fas fa-copy"></i> Copy
                    </button>
                    <a href="/download_summary?text={{ summary | urlencode }}" class="action-btn download-btn" download>
                        <i class="fas fa-download"></i> Download TXT
                    </a>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        function copySummary() {
            const summaryText = document.getElementById('summaryText').innerText;
            navigator.clipboard.writeText(summaryText).then(() => {
                alert('Summary copied to clipboard!');
            }).catch(err => {
                alert('Failed to copy: ' + err);
            });
        }
    </script>
</body>
</html>"""

    # Quiz template
    quiz_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Quiz Generator - StudyGenie</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --dark: #0f172a; --light: #f8fafc; --gray: #64748b; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, var(--dark) 0%, #1e1b4b 100%); color: var(--light); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        nav { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 20px; padding: 15px; margin-bottom: 30px; text-align: center; }
        nav a { color: var(--light); text-decoration: none; margin: 0 15px; padding: 8px 20px; background: rgba(99, 102, 241, 0.1); border-radius: 20px; }
        .hero { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 25px; padding: 50px; }
        .form-group { margin-bottom: 25px; }
        .form-group input, .form-group select { width: 100%; padding: 15px; background: rgba(15, 23, 42, 0.8); border: 2px solid rgba(99, 102, 241, 0.3); border-radius: 15px; color: var(--light); font-size: 1rem; }
        .btn { background: linear-gradient(135deg, var(--primary), #8b5cf6); color: white; padding: 15px 40px; border: none; border-radius: 25px; cursor: pointer; width: 100%; margin: 20px 0; }
        .question-item { background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); padding: 25px; margin: 20px 0; border-radius: 20px; }
        .save-quiz-btn {
            background: rgba(6, 182, 212, 0.2);
            border: 1px solid rgba(6, 182, 212, 0.4);
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            cursor: pointer;
            margin-top: 20px;
            font-size: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="/"><i class="fas fa-home"></i> Home</a>
            <a href="/upload"><i class="fas fa-file-pdf"></i> Upload</a>
            <a href="/quiz"><i class="fas fa-brain"></i> Quiz</a>
            <a href="/schedule"><i class="fas fa-calendar"></i> Schedule</a>
            <a href="/history"><i class="fas fa-history"></i> History</a>
        </nav>

        <div class="hero">
            <h2 style="text-align: center; margin-bottom: 30px;"><i class="fas fa-brain"></i> AI Quiz Generator</h2>

            <form id="quizForm">
                <div class="form-group">
                    <input type="text" id="topic" placeholder="Enter study topic (e.g., Data Structures)" required>
                </div>
                <div class="form-group">
                    <select id="numQuestions">
                        <option value="3">3 Questions</option>
                        <option value="5" selected>5 Questions</option>
                        <option value="8">8 Questions</option>
                    </select>
                </div>
                <button type="submit" class="btn">
                    <i class="fas fa-magic"></i> Generate Quiz
                </button>
            </form>

            <div id="quizResults" style="display:none;">
                <h3 style="text-align: center; margin: 30px 0;">📋 Your AI-Generated Quiz</h3>
                <div id="questionsList"></div>
                <button onclick="saveQuizToHistory()" class="save-quiz-btn">
                    <i class="fas fa-save"></i> Save to History
                </button>
            </div>
        </div>
    </div>

    <script>
        let currentQuiz = null;

        document.getElementById('quizForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const topic = document.getElementById('topic').value;
            const numQuestions = document.getElementById('numQuestions').value;

            try {
                const response = await fetch('/generate_quiz', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({topic, num_questions: parseInt(numQuestions)})
                });
                const data = await response.json();
                currentQuiz = data.questions;
                displayQuiz(data.questions);
            } catch (error) {
                alert('Error generating quiz');
            }
        });

        function displayQuiz(questions) {
            const questionsList = document.getElementById('questionsList');
            questionsList.innerHTML = '';

            questions.forEach((q) => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question-item';
                questionDiv.innerHTML = `
                    <strong>Q${q.id}:</strong> ${q.question}
                    <br><br>
                    <textarea placeholder="Write your answer here..." style="width: 100%; height: 80px; padding: 10px; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; color: white;"></textarea>
                `;
                questionsList.appendChild(questionDiv);
            });

            document.getElementById('quizResults').style.display = 'block';
        }

        function saveQuizToHistory() {
            if (!currentQuiz) return;
            fetch('/save_quiz', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    topic: document.getElementById('topic').value,
                    questions: currentQuiz
                })
            }).then(r => r.json()).then(data => {
                if (data.success) alert('✅ Quiz saved to history!');
                else alert('❌ Failed to save quiz');
            });
        }
    </script>
</body>
</html>"""

    # Schedule template
    schedule_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Study Planner - StudyGenie</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --dark: #0f172a; --light: #f8fafc; --gray: #64748b; --success: #10b981; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, var(--dark) 0%, #1e1b4b 100%); color: var(--light); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        nav { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 20px; padding: 15px; margin-bottom: 30px; text-align: center; }
        nav a { color: var(--light); text-decoration: none; margin: 0 15px; padding: 8px 20px; background: rgba(99, 102, 241, 0.1); border-radius: 20px; }
        .hero { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 25px; padding: 50px; }
        .form-group { margin-bottom: 25px; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 15px; background: rgba(15, 23, 42, 0.8); border: 2px solid rgba(99, 102, 241, 0.3); border-radius: 15px; color: var(--light); font-size: 1rem; font-family: inherit; }
        .form-group textarea { min-height: 120px; }
        .btn { background: linear-gradient(135deg, var(--primary), #8b5cf6); color: white; padding: 15px 40px; border: none; border-radius: 25px; cursor: pointer; width: 100%; margin: 20px 0; }
        .schedule-item { background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); padding: 25px; margin: 15px 0; border-radius: 20px; }
        .priority { padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
        .priority-high { background: #ef4444; color: white; }
        .priority-medium { background: #f59e0b; color: white; }
        .priority-normal { background: var(--success); color: white; }
        .error { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 20px; border-radius: 10px; color: #fca5a5; }
        .export-btn {
            background: rgba(6, 182, 212, 0.2);
            border: 1px solid rgba(6, 182, 212, 0.4);
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            cursor: pointer;
            margin-top: 20px;
            font-size: 1rem;
            display: block;
            width: fit-content;
            margin: 20px auto 0;
        }
        .save-schedule-btn {
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            cursor: pointer;
            margin-top: 10px;
            font-size: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="/"><i class="fas fa-home"></i> Home</a>
            <a href="/upload"><i class="fas fa-file-pdf"></i> Upload</a>
            <a href="/quiz"><i class="fas fa-brain"></i> Quiz</a>
            <a href="/schedule"><i class="fas fa-calendar"></i> Schedule</a>
            <a href="/history"><i class="fas fa-history"></i> History</a>
        </nav>

        <div class="hero">
            <h2 style="text-align: center; margin-bottom: 30px;"><i class="fas fa-calendar-alt"></i> AI Study Planner</h2>

            <form id="scheduleForm">
                <div class="form-group">
                    <label style="color: var(--light); margin-bottom: 10px; display: block;">📖 Your Subjects (one per line):</label>
                    <textarea id="subjects" placeholder="Data Structures&#10;Algorithms&#10;Database Systems&#10;Computer Networks" required></textarea>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="form-group">
                        <label style="color: var(--light); margin-bottom: 10px; display: block;">📆 Exam Date:</label>
                        <input type="date" id="examDate" required>
                    </div>

                    <div class="form-group">
                        <label style="color: var(--light); margin-bottom: 10px; display: block;">⏰ Hours per Day:</label>
                        <select id="hoursPerDay">
                            <option value="2">2 hours</option>
                            <option value="4" selected>4 hours</option>
                            <option value="6">6 hours</option>
                            <option value="8">8 hours</option>
                        </select>
                    </div>
                </div>

                <button type="submit" class="btn">
                    <i class="fas fa-magic"></i> Generate Schedule
                </button>
            </form>

            <div id="scheduleResults" style="display:none;">
                <h3 style="text-align: center; margin: 30px 0;">📊 Your Personalized Study Plan</h3>
                <div id="scheduleList"></div>
                <button onclick="saveScheduleToHistory()" class="save-schedule-btn">
                    <i class="fas fa-save"></i> Save to History
                </button>
                <button onclick="exportScheduleToCSV()" class="export-btn">
                    <i class="fas fa-file-csv"></i> Export as CSV
                </button>
            </div>

            <div id="error" class="error" style="display:none;"></div>
        </div>
    </div>

    <script>
        // Set minimum date to today
        document.getElementById('examDate').min = new Date().toISOString().split('T')[0];

        let currentSchedule = null;

        document.getElementById('scheduleForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const subjectsText = document.getElementById('subjects').value;
            const subjects = subjectsText.split('\\n').filter(s => s.trim().length > 0);
            const examDate = document.getElementById('examDate').value;
            const hoursPerDay = parseInt(document.getElementById('hoursPerDay').value);

            if (subjects.length === 0) {
                document.getElementById('error').textContent = 'Please enter at least one subject';
                document.getElementById('error').style.display = 'block';
                return;
            }

            try {
                const response = await fetch('/generate_schedule', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({subjects, exam_date: examDate, hours_per_day: hoursPerDay})
                });

                const data = await response.json();
                if (data.error) {
                    document.getElementById('error').textContent = data.error;
                    document.getElementById('error').style.display = 'block';
                } else {
                    currentSchedule = data.schedule;
                    displaySchedule(data.schedule);
                    document.getElementById('error').style.display = 'none';
                }
            } catch (error) {
                document.getElementById('error').textContent = 'Error generating schedule. Please try again.';
                document.getElementById('error').style.display = 'block';
            }
        });

        function displaySchedule(schedule) {
            const scheduleList = document.getElementById('scheduleList');
            scheduleList.innerHTML = '';

            if (schedule && schedule.length > 0) {
                schedule.forEach(item => {
                    const scheduleItem = document.createElement('div');
                    scheduleItem.className = 'schedule-item';
                    scheduleItem.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <strong style="font-size: 1.2rem;">${item.subject}</strong>
                            <span class="priority priority-${item.priority.toLowerCase()}">${item.priority}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px;">
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; color: var(--primary);">${item.daily_hours}h</div>
                                <div style="color: var(--gray);">Daily</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; color: var(--primary);">${item.recommended_hours}h</div>
                                <div style="color: var(--gray);">Total</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; color: var(--primary);">${item.days_allocated || 'N/A'}</div>
                                <div style="color: var(--gray);">Days</div>
                            </div>
                        </div>
                        <div style="padding: 15px; background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 12px;">
                            💡 ${item.study_tips}
                        </div>
                    `;
                    scheduleList.appendChild(scheduleItem);
                });

                document.getElementById('scheduleResults').style.display = 'block';
            }
        }

        function saveScheduleToHistory() {
            if (!currentSchedule) return;
            const subjects = Array.from(document.querySelectorAll('#scheduleList .schedule-item')).map(el => 
                el.querySelector('strong').innerText
            );
            fetch('/save_schedule', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    subjects: subjects,
                    exam_date: document.getElementById('examDate').value,
                    hours_per_day: parseInt(document.getElementById('hoursPerDay').value),
                    schedule: currentSchedule
                })
            }).then(r => r.json()).then(data => {
                if (data.success) alert('✅ Schedule saved to history!');
                else alert('❌ Failed to save schedule');
            });
        }

        function exportScheduleToCSV() {
            if (!currentSchedule) return;
            const csvContent = "data:text/csv;charset=utf-8," 
                + "Subject,Priority,Daily Hours,Total Hours,Days,Study Tips\\n"
                + currentSchedule.map(item => 
                    `"${item.subject}","${item.priority}",${item.daily_hours},${item.recommended_hours},${item.days_allocated},"${item.study_tips.replace(/"/g, '""')}"`.replace(/#/g, '')
                ).join("\\n");

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "study_schedule.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>"""

    # History template
    history_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>History - StudyGenie</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --dark: #0f172a; --light: #f8fafc; --gray: #64748b; --danger: #ef4444; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, var(--dark) 0%, #1e1b4b 100%); color: var(--light); min-height: 100vh; }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        nav { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 20px; padding: 15px; margin-bottom: 30px; text-align: center; }
        nav a { color: var(--light); text-decoration: none; margin: 0 15px; padding: 8px 20px; background: rgba(99, 102, 241, 0.1); border-radius: 20px; }
        .hero { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 25px; padding: 40px; }
        h2 { text-align: center; margin-bottom: 30px; }
        .history-section { margin-bottom: 40px; }
        .history-item { background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); padding: 20px; margin: 15px 0; border-radius: 15px; }
        .history-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .delete-btn { background: rgba(239, 68, 68, 0.2); color: white; border: none; padding: 5px 10px; border-radius: 10px; cursor: pointer; }
        .clear-all-btn { 
            background: var(--danger); 
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 20px; 
            cursor: pointer; 
            margin: 30px auto 0; 
            display: block;
            font-weight: 600;
        }
        .empty-state { text-align: center; padding: 40px; color: var(--gray); }
        .download-link { color: var(--primary); text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="/"><i class="fas fa-home"></i> Home</a>
            <a href="/upload"><i class="fas fa-file-pdf"></i> Upload</a>
            <a href="/quiz"><i class="fas fa-brain"></i> Quiz</a>
            <a href="/schedule"><i class="fas fa-calendar"></i> Schedule</a>
            <a href="/history"><i class="fas fa-history"></i> History</a>
        </nav>

        <div class="hero">
            <h2><i class="fas fa-history"></i> Your Study History</h2>

            <div class="history-section">
                <h3>📄 Summaries</h3>
                {% if summaries and summaries|length > 0 %}
                    {% for item in summaries %}
                    <div class="history-item">
                        <div class="history-header">
                            <strong>Generated: {{ item.timestamp }}</strong>
                            <button onclick="deleteItem('summaries', {{ loop.index0 }})" class="delete-btn">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </div>
                        <div>{{ item.summary[:200] }}{% if item.summary|length > 200 %}...{% endif %}</div>
                        <a href="/download_summary?text={{ item.summary | urlencode }}" class="download-link">
                            <i class="fas fa-download"></i> Download TXT
                        </a>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="empty-state">No summaries saved yet.</div>
                {% endif %}
            </div>

            <div class="history-section">
                <h3>🧠 Quizzes</h3>
                {% if quizzes and quizzes|length > 0 %}
                    {% for item in quizzes %}
                    <div class="history-item">
                        <div class="history-header">
                            <strong>{{ item.topic }} ({{ item.questions|length }} Qs) - {{ item.timestamp }}</strong>
                            <button onclick="deleteItem('quizzes', {{ loop.index0 }})" class="delete-btn">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </div>
                        {% for q in item.questions %}
                        <div style="margin: 10px 0; padding-left: 15px; border-left: 3px solid var(--primary);">
                            Q{{ q.id }}: {{ q.question }}
                        </div>
                        {% endfor %}
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="empty-state">No quizzes saved yet.</div>
                {% endif %}
            </div>

            <div class="history-section">
                <h3>📅 Schedules</h3>
                {% if schedules and schedules|length > 0 %}
                    {% for item in schedules %}
                    <div class="history-item">
                        <div class="history-header">
                            <strong>Exam: {{ item.exam_date }} | {{ item.hours_per_day }}h/day - {{ item.timestamp }}</strong>
                            <button onclick="deleteItem('schedules', {{ loop.index0 }})" class="delete-btn">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </div>
                        {% for s in item.schedule %}
                        <div style="margin: 15px 0; padding: 10px; background: rgba(6, 182, 212, 0.1); border-radius: 8px;">
                            <strong>{{ s.subject }}</strong> ({{ s.priority }}) - {{ s.daily_hours }}h/day → {{ s.recommended_hours }}h total
                            <div style="font-size: 0.9rem; margin-top: 5px; color: var(--gray);">💡 {{ s.study_tips }}</div>
                        </div>
                        {% endfor %}
                        <a href="#" onclick="exportHistorySchedule({{ loop.index0 }}); return false;" class="download-link">
                            <i class="fas fa-file-csv"></i> Export as CSV
                        </a>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="empty-state">No schedules saved yet.</div>
                {% endif %}
            </div>

            <button onclick="clearAllHistory()" class="clear-all-btn">
                <i class="fas fa-trash-alt"></i> Clear All History
            </button>
        </div>
    </div>

    <script>
        async function deleteItem(type, index) {
            if (!confirm('Are you sure you want to delete this item?')) return;
            
            const response = await fetch('/delete_history', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type, index})
            });
            
            if (response.ok) {
                location.reload();
            } else {
                alert('Failed to delete item');
            }
        }

        async function clearAllHistory() {
            if (!confirm('Are you sure you want to clear ALL history? This cannot be undone.')) return;
            
            const response = await fetch('/clear_history', {method: 'POST'});
            
            if (response.ok) {
                location.reload();
            } else {
                alert('Failed to clear history');
            }
        }

        function exportHistorySchedule(index) {
            fetch('/get_schedule_csv/' + index)
                .then(response => response.text())
                .then(csvContent => {
                    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                    const link = document.createElement("a");
                    const url = URL.createObjectURL(blob);
                    link.setAttribute("href", url);
                    link.setAttribute("download", "study_schedule_export.csv");
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });
        }
    </script>
</body>
</html>"""

    # Write templates
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('templates/upload.html', 'w', encoding='utf-8') as f:
        f.write(upload_html)
    with open('templates/quiz.html', 'w', encoding='utf-8') as f:
        f.write(quiz_html)
    with open('templates/schedule.html', 'w', encoding='utf-8') as f:
        f.write(schedule_html)
    with open('templates/history.html', 'w', encoding='utf-8') as f:
        f.write(history_html)

create_enhanced_templates()

@app.route('/')
def home():
    init_history()
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    init_history()
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return render_template('upload.html', error='No file selected')

            file = request.files['file']
            if file.filename == '':
                return render_template('upload.html', error='No file selected')

            if not file.filename.lower().endswith('.pdf'):
                return render_template('upload.html', error='Please upload a PDF file only')

            # ✅ FIXED: Check file size without consuming stream
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)

            if size > 5 * 1024 * 1024:
                return render_template('upload.html', error='File too large. Please upload files smaller than 5MB')

            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract text
            text = extract_text_from_pdf(filepath)
            if "Error" in text or "⚠️" in text:
                return render_template('upload.html', error=text)

            # Generate summary
            summary = generate_simple_summary(text)

            # Save to history
            history_item = {
                'filename': filename,
                'summary': summary,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            session['history']['summaries'].append(history_item)
            session.modified = True

            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass

            return render_template('upload.html', summary=summary)

        except Exception as e:
            return render_template('upload.html', error=f'An error occurred: {str(e)}')

    return render_template('upload.html')

@app.route('/download_summary')
def download_summary():
    text = request.args.get('text', '')
    if not text:
        return "No text provided", 400

    # Create in-memory file
    from io import StringIO
    output = StringIO()
    output.write(text)
    output.seek(0)

    return send_file(
        output,
        mimetype='text/plain',
        as_attachment=True,
        download_name='summary.txt'
    )

@app.route('/quiz')
def quiz():
    init_history()
    return render_template('quiz.html')

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    try:
        topic = request.json.get('topic', '').strip()
        num_questions = request.json.get('num_questions', 5)

        if not topic:
            return jsonify({'error': 'Please enter a topic'})

        questions = generate_quiz_questions(topic, num_questions)
        return jsonify({'questions': questions})

    except Exception as e:
        return jsonify({'error': f'Failed to generate quiz: {str(e)}'})

@app.route('/save_quiz', methods=['POST'])
def save_quiz():
    init_history()
    try:
        data = request.json
        quiz_data = {
            'topic': data['topic'],
            'questions': data['questions'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        session['history']['quizzes'].append(quiz_data)
        session.modified = True
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/schedule')
def schedule():
    init_history()
    return render_template('schedule.html')

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    try:
        data = request.json
        subjects = data.get('subjects', [])
        exam_date = data.get('exam_date', '').strip()
        hours_per_day = data.get('hours_per_day', 4)

        if not subjects or len(subjects) == 0:
            return jsonify({'error': 'Please enter at least one subject'})

        if not exam_date:
            return jsonify({'error': 'Please select an exam date'})

        schedule = create_study_schedule(subjects, exam_date, hours_per_day)

        if isinstance(schedule, list) and len(schedule) > 0 and 'error' in schedule[0]:
            return jsonify({'error': schedule[0]['error']})

        return jsonify({'schedule': schedule})

    except Exception as e:
        return jsonify({'error': f'Failed to generate schedule: {str(e)}'})

@app.route('/save_schedule', methods=['POST'])
def save_schedule():
    init_history()
    try:
        data = request.json
        schedule_data = {
            'subjects': data['subjects'],
            'exam_date': data['exam_date'],
            'hours_per_day': data['hours_per_day'],
            'schedule': data['schedule'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        session['history']['schedules'].append(schedule_data)
        session.modified = True
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_schedule_csv/<int:index>')
def get_schedule_csv(index):
    init_history()
    try:
        if index >= len(session['history']['schedules']):
            return "Schedule not found", 404
            
        schedule = session['history']['schedules'][index]['schedule']
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Subject', 'Priority', 'Daily Hours', 'Total Hours', 'Days', 'Study Tips'])
        
        for item in schedule:
            writer.writerow([
                item['subject'],
                item['priority'],
                item['daily_hours'],
                item['recommended_hours'],
                item['days_allocated'],
                item['study_tips']
            ])
            
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=schedule_export.csv'
        }
    except Exception as e:
        return str(e), 500

@app.route('/delete_history', methods=['POST'])
def delete_history():
    init_history()
    try:
        data = request.json
        hist_type = data['type']
        index = data['index']
        
        if hist_type in session['history'] and 0 <= index < len(session['history'][hist_type]):
            session['history'][hist_type].pop(index)
            session.modified = True
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid index'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    init_history()
    try:
        session['history'] = {
            'summaries': [],
            'quizzes': [],
            'schedules': []
        }
        session.modified = True
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/history')
def history():
    init_history()
    return render_template(
        'history.html',
        summaries=session['history']['summaries'],
        quizzes=session['history']['quizzes'],
        schedules=session['history']['schedules']
    )

# ✅ FIXED: Robust PDF extraction with graceful fallback
def extract_text_from_pdf(filepath):
    """Extract text from PDF with fallback and better error handling"""
    try:
        # Try PyPDF2 first
        try:
            import PyPDF2
        except ImportError:
            # Fallback: return dummy text for testing or install instruction
            return ("⚠️ PyPDF2 not installed. Install it using:\n"
                    "pip install PyPDF2\n\n"
                    "For now, here's sample extracted text:\n\n"
                    "This is a sample summary because PDF processing is not available. "
                    "The document discusses key concepts in computer science including algorithms, "
                    "data structures, and software engineering principles. It emphasizes practical "
                    "implementation and problem-solving techniques.")

        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            if len(pdf_reader.pages) == 0:
                return "Error: PDF file appears to be empty"

            text = ""
            # Read first 3 pages only to avoid memory issues
            for page_num in range(min(3, len(pdf_reader.pages))):
                try:
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text += page_text.strip() + " "
                except Exception as page_error:
                    continue  # Skip problematic pages

            if not text.strip():
                return "Error: Could not extract readable text from PDF. The file may be scanned or encrypted."

            return text.strip()[:3000]  # Limit to first 3000 characters

    except Exception as e:
        return f"Error processing PDF: {str(e)}. Please ensure it's a valid text-based PDF."

def generate_simple_summary(text):
    """Generate summary with better text processing"""
    try:
        if len(text) < 50:
            return "Text too short to summarize effectively. Please upload a document with more content."

        # Clean the text
        text = text.replace('\n', ' ').replace('\t', ' ')

        # Split into sentences
        sentences = []
        for sentence in text.split('.'):
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:  # Filter reasonable sentences
                sentences.append(sentence)

        if len(sentences) < 2:
            return f"Document Summary: {text[:400]}..."

        # Take first few sentences and key sentences
        summary_sentences = sentences[:2]  # First 2 sentences

        # Look for sentences with key academic terms
        key_terms = ['definition', 'concept', 'theory', 'principle', 'method', 'approach', 'algorithm', 'formula']
        for sentence in sentences[2:]:
            if len(summary_sentences) >= 5:
                break
            if any(term in sentence.lower() for term in key_terms):
                summary_sentences.append(sentence)

        # Add more sentences if we don't have enough
        while len(summary_sentences) < 4 and len(sentences) > len(summary_sentences):
            summary_sentences.append(sentences[len(summary_sentences)])

        summary = '. '.join(summary_sentences[:5]) + '.'

        # If summary is too short, add more content
        if len(summary) < 100:
            summary = f"Key Points from Document: {text[:500]}..."

        return summary

    except Exception as e:
        return f"Summary generation error: {str(e)}. Here's the beginning of the document: {text[:300]}..."

def generate_quiz_questions(topic, num_questions):
    """Generate quiz questions - this function works fine"""
    question_templates = [
        f"What are the key concepts and fundamentals of {topic}?",
        f"Explain the significance and applications of {topic}.",
        f"List three important practical applications of {topic}.",
        f"How does {topic} connect to other related concepts in your field?",
        f"What are the main challenges when working with {topic}?",
        f"Describe how you would implement or use {topic} in practice.",
        f"What are the core principles underlying {topic}?",
        f"How would you solve a complex problem involving {topic}?"
    ]

    questions = []
    selected = random.sample(question_templates, min(num_questions, len(question_templates)))

    for i, template in enumerate(selected):
        questions.append({
            "id": i + 1,
            "question": template,
            "type": "short_answer" if i % 2 == 0 else "essay",
            "points": 5
        })

    return questions

# ✅ FIXED: Improved error messages and logic
def create_study_schedule(subjects, exam_date, hours_per_day):
    """Generate study schedule with better error handling"""
    try:
        # Parse exam date
        exam_date_obj = datetime.strptime(exam_date, '%Y-%m-%d')
        today = datetime.now()
        days_until_exam = max(1, (exam_date_obj - today).days)

        if days_until_exam <= 0:
            return [{"error": "❌ Exam date must be in the future. Please select a date after today."}]

        if days_until_exam > 365:
            return [{"error": "📅 Exam date is too far away (over 1 year). Please pick a closer date."}]

        if not subjects or len(subjects) == 0:
            return [{"error": "📚 Please provide at least one subject to study."}]

        schedule = []

        # Calculate hours per subject
        total_available_hours = days_until_exam * hours_per_day
        hours_per_subject = max(1, total_available_hours // len(subjects))
        daily_hours_per_subject = max(1, hours_per_day // len(subjects))

        for i, subject in enumerate(subjects):
            # Assign priority
            if i < len(subjects) // 3:
                priority = "High"
            elif i < 2 * len(subjects) // 3:
                priority = "Medium"
            else:
                priority = "Normal"

            schedule.append({
                'subject': subject.strip(),
                'recommended_hours': hours_per_subject,
                'daily_hours': daily_hours_per_subject,
                'priority': priority,
                'study_tips': get_study_tips(subject.strip()),
                'days_allocated': days_until_exam
            })

        return schedule

    except ValueError as e:
        return [{"error": "Invalid date format. Please use YYYY-MM-DD format."}]
    except Exception as e:
        return [{"error": f"Failed to create schedule: {str(e)}"}]

def get_study_tips(subject):
    """Get subject-specific study tips"""
    tips_map = {
        'math': 'Practice problem-solving daily and focus on understanding concepts',
        'physics': 'Understand theory first, then solve numerical problems',
        'chemistry': 'Memorize formulas and practice chemical equations regularly',
        'computer': 'Code regularly and practice algorithmic thinking',
        'data structures': 'Implement each data structure and analyze time complexity',
        'algorithms': 'Focus on problem-solving patterns and complexity analysis',
        'database': 'Practice SQL queries and understand database design',
        'networks': 'Study protocols and understand network layers',
        'operating': 'Focus on system concepts and process management',
        'software': 'Practice coding and understand software design principles',
        'web': 'Build projects and practice frontend/backend development',
        'machine learning': 'Understand math foundations and implement algorithms',
        'artificial intelligence': 'Study algorithms and work with datasets'
    }

    subject_lower = subject.lower()

    for key, tip in tips_map.items():
        if key in subject_lower:
            return tip

    return f"Create a structured study plan with regular practice and revision for {subject}"

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 STUDYGENIE ULTIMATE EDITION STARTING...")
    print("="*60)
    print("✨ Features:")
    print("   • PDF Summarizer (with TXT download)")
    print("   • AI Quiz Generator (save to history)")
    print("   • Smart Study Planner (export as CSV)")
    print("   • Full History Management")
    print("   • Session-based User Memory (no login needed)")
    print("\n📱 Open: http://localhost:5000")
    print("📚 Start studying smarter today!\n")
app.run(debug=True, port=5000, host='0.0.0.0')# In your project folder


