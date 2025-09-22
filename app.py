
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import PyPDF2
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)
app.secret_key = 'studygenie_secret_key_2025'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create directories
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def create_enhanced_templates():
    # Enhanced Index Template with Dark Theme and Animations
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
            --darker: #020617;
            --light: #f8fafc;
            --gray: #64748b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, #1e1b4b 100%);
            color: var(--light);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated Background */
        .animated-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, #1e1b4b 100%);
        }

        .animated-bg::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="a" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="%236366f1" stop-opacity="0.1"/><stop offset="100%" stop-color="%236366f1" stop-opacity="0"/></radialGradient></defs><circle cx="200" cy="200" r="100" fill="url(%23a)" class="floating-circle"><animateTransform attributeName="transform" type="translate" values="0,0;50,30;0,0" dur="6s" repeatCount="indefinite"/></circle><circle cx="800" cy="300" r="150" fill="url(%23a)" class="floating-circle"><animateTransform attributeName="transform" type="translate" values="0,0;-30,50;0,0" dur="8s" repeatCount="indefinite"/></circle></svg>');
            animation: float 10s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Header with Glow Effect */
        header {
            text-align: center;
            margin-bottom: 50px;
            position: relative;
        }

        .logo {
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
            animation: glow 2s ease-in-out infinite alternate;
            margin-bottom: 10px;
        }

        @keyframes glow {
            from { text-shadow: 0 0 30px rgba(99, 102, 241, 0.5); }
            to { text-shadow: 0 0 50px rgba(99, 102, 241, 0.8), 0 0 70px rgba(139, 92, 246, 0.4); }
        }

        .tagline {
            font-size: 1.4rem;
            color: var(--gray);
            font-weight: 300;
            letter-spacing: 1px;
        }

        /* Navigation */
        nav {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 20px;
            padding: 15px 0;
            margin-bottom: 50px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        nav ul {
            list-style: none;
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }

        nav a {
            color: var(--light);
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 25px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 500;
            position: relative;
            overflow: hidden;
        }

        nav a::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }

        nav a:hover::before {
            left: 100%;
        }

        nav a:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 27, 75, 0.9));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 25px;
            padding: 60px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.05) 0%, transparent 50%);
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .hero-content {
            position: relative;
            z-index: 2;
        }

        .hero h2 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-description {
            font-size: 1.2rem;
            color: var(--gray);
            margin-bottom: 50px;
            line-height: 1.6;
        }

        /* Feature Cards */
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }

        .feature-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 27, 75, 0.8));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
            border-radius: 20px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: -1;
        }

        .feature-card:hover::before {
            opacity: 1;
        }

        .feature-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        }

        .feature-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .feature-card h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--light);
        }

        .feature-card p {
            color: var(--gray);
            margin-bottom: 25px;
            line-height: 1.6;
        }

        /* Buttons */
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            cursor: pointer;
            font-size: 1rem;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
        }

        /* Stats Section */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin: 50px 0;
        }

        .stat-item {
            text-align: center;
            padding: 20px;
            background: rgba(99, 102, 241, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
            color: var(--accent);
            display: block;
        }

        .stat-label {
            color: var(--gray);
            font-weight: 500;
            margin-top: 5px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container { padding: 15px; }
            .logo { font-size: 2.5rem; }
            .hero { padding: 30px; }
            .hero h2 { font-size: 2rem; }
            .features { grid-template-columns: 1fr; gap: 20px; }
            .feature-card { padding: 30px; }
            nav ul { flex-direction: column; align-items: center; gap: 15px; }
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: var(--primary);
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="animated-bg"></div>
    <div class="container">
        <header>
            <div class="logo">🧞‍♂️ StudyGenie</div>
            <div class="tagline">Your AI-Powered Study Companion for Academic Excellence</div>
        </header>

        <nav>
            <ul>
                <li><a href="/"><i class="fas fa-home"></i> Home</a></li>
                <li><a href="/upload"><i class="fas fa-file-pdf"></i> Smart Summarizer</a></li>
                <li><a href="/quiz"><i class="fas fa-brain"></i> Quiz Generator</a></li>
                <li><a href="/schedule"><i class="fas fa-calendar-alt"></i> Study Planner</a></li>
            </ul>
        </nav>

        <main>
            <div class="hero">
                <div class="hero-content">
                    <h2>Transform Your Study Experience with AI</h2>
                    <p class="hero-description">
                        StudyGenie harnesses the power of artificial intelligence to revolutionize how IIT students learn, 
                        practice, and excel in their academic journey. From intelligent PDF summarization to personalized 
                        quiz generation, we've got your study needs covered.
                    </p>

                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-number">10x</span>
                            <span class="stat-label">Faster Learning</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">95%</span>
                            <span class="stat-label">Better Retention</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">5+</span>
                            <span class="stat-label">Hours Saved Daily</span>
                        </div>
                    </div>

                    <div class="features">
                        <div class="feature-card">
                            <div class="feature-icon">📄</div>
                            <h3>AI-Powered PDF Summarizer</h3>
                            <p>Upload lengthy lecture notes, research papers, or textbook chapters and get concise, 
                               intelligent summaries that highlight key concepts and important information.</p>
                            <a href="/upload" class="btn">
                                <i class="fas fa-upload"></i> Start Summarizing
                            </a>
                        </div>

                        <div class="feature-card">
                            <div class="feature-icon">🧠</div>
                            <h3>Intelligent Quiz Generator</h3>
                            <p>Generate unlimited practice questions tailored to your study topics. Our AI creates 
                               diverse question types to test your understanding and reinforce learning.</p>
                            <a href="/quiz" class="btn">
                                <i class="fas fa-play"></i> Create Quiz
                            </a>
                        </div>

                        <div class="feature-card">
                            <div class="feature-icon">📊</div>
                            <h3>Smart Study Scheduler</h3>
                            <p>Get personalized study schedules optimized for your subjects, deadlines, and learning pace. 
                               Maximize productivity with AI-driven time management strategies.</p>
                            <a href="/schedule" class="btn">
                                <i class="fas fa-calendar"></i> Plan Studies
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <footer style="text-align: center; margin-top: 60px; padding: 30px; color: var(--gray); border-top: 1px solid rgba(99, 102, 241, 0.2);">
            <p>&copy; 2025 StudyGenie - Built for AIGNITION 2025 | Empowering IIT Patna Students with AI</p>
        </footer>
    </div>

    <script>
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add loading states to buttons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const icon = this.querySelector('i');
                if (icon) {
                    icon.className = 'loading';
                }
            });
        });

        // Add intersection observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.feature-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(card);
        });
    </script>
</body>
</html>"""

    # Enhanced Upload Template
    upload_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Summarizer - StudyGenie</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --accent: #06b6d4;
            --dark: #0f172a;
            --darker: #020617;
            --light: #f8fafc;
            --gray: #64748b;
            --success: #10b981;
            --warning: #f59e0b;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, #1e1b4b 100%);
            color: var(--light);
            min-height: 100vh;
        }

        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }

        /* Navigation */
        nav {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 20px;
            padding: 15px 0;
            margin-bottom: 30px;
            text-align: center;
        }

        nav a {
            color: var(--light);
            text-decoration: none;
            margin: 0 15px;
            padding: 8px 20px;
            background: rgba(99, 102, 241, 0.1);
            border-radius: 20px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: all 0.3s;
        }

        nav a:hover {
            background: rgba(99, 102, 241, 0.2);
            transform: translateY(-2px);
        }

        /* Main Content */
        .hero {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 27, 75, 0.9));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }

        .hero h2 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }

        .hero-subtitle {
            text-align: center;
            color: var(--gray);
            font-size: 1.1rem;
            margin-bottom: 40px;
        }

        /* Upload Area */
        .upload-area {
            border: 2px dashed rgba(99, 102, 241, 0.5);
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
            padding: 60px 40px;
            text-align: center;
            border-radius: 20px;
            margin: 30px 0;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .upload-area:hover {
            border-color: rgba(99, 102, 241, 0.8);
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            transform: translateY(-5px);
        }

        .upload-icon {
            font-size: 4rem;
            color: var(--primary);
            margin-bottom: 20px;
            animation: bounce 2s ease-in-out infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .upload-area h3 {
            font-size: 1.5rem;
            margin-bottom: 10px;
            color: var(--light);
        }

        .upload-area p {
            color: var(--gray);
            margin-bottom: 20px;
        }

        .file-input {
            width: 100%;
            padding: 15px;
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 15px;
            color: var(--light);
            margin-bottom: 20px;
        }

        .btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        /* Summary Results */
        .summary-result {
            margin-top: 40px;
            animation: fadeInUp 0.6s ease-out;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .summary-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        .summary-header i {
            font-size: 2rem;
            color: var(--success);
            margin-right: 15px;
        }

        .summary-box {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1));
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 30px;
            border-radius: 20px;
            line-height: 1.8;
            font-size: 1.1rem;
            color: var(--light);
            position: relative;
            overflow: hidden;
        }

        .summary-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.03) 0%, transparent 50%);
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .actions {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            justify-content: center;
        }

        .btn-secondary {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            border: 1px solid rgba(99, 102, 241, 0.4);
        }

        /* Loading States */
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(99, 102, 241, 0.3);
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .container { padding: 15px; }
            .hero { padding: 30px 25px; }
            .hero h2 { font-size: 2rem; }
            .upload-area { padding: 40px 25px; }
            .actions { flex-direction: column; }
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
        </nav>

        <div class="hero">
            <h2><i class="fas fa-magic"></i> AI PDF Summarizer</h2>
            <p class="hero-subtitle">Transform lengthy documents into concise, intelligent summaries in seconds</p>

            <form method="post" enctype="multipart/form-data" id="uploadForm">
                <div class="upload-area">
                    <div class="upload-icon">
                        <i class="fas fa-cloud-upload-alt"></i>
                    </div>
                    <h3>Upload Your Study Materials</h3>
                    <p>Drag & drop your PDF file or click to browse</p>
                    <input type="file" name="file" accept=".pdf" required class="file-input">
                </div>
                <button type="submit" class="btn">
                    <i class="fas fa-sparkles"></i> Generate Summary
                </button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI is analyzing your document... Please wait</p>
            </div>

            {% if summary %}
            <div class="summary-result">
                <div class="summary-header">
                    <i class="fas fa-check-circle"></i>
                    <h3>📝 Summary Generated Successfully</h3>
                </div>
                <div class="summary-box">
                    <div style="position: relative; z-index: 2;">{{ summary }}</div>
                </div>
                <div class="actions">
                    <button onclick="copySummary()" class="btn btn-secondary">
                        <i class="fas fa-copy"></i> Copy Summary
                    </button>
                    <a href="/quiz" class="btn">
                        <i class="fas fa-arrow-right"></i> Generate Quiz
                    </a>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        // Form submission with loading state
        document.getElementById('uploadForm').addEventListener('submit', function() {
            document.getElementById('loading').style.display = 'block';
            document.querySelector('.btn[type="submit"]').disabled = true;
        });

        // Copy summary function
        function copySummary() {
            const summaryText = document.querySelector('.summary-box').innerText;
            navigator.clipboard.writeText(summaryText).then(function() {
                // Show success feedback
                const btn = event.target.closest('button');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';

                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.background = '';
                }, 2000);
            });
        }

        // File input styling
        document.querySelector('input[type="file"]').addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                const uploadArea = document.querySelector('.upload-area');
                uploadArea.style.borderColor = 'rgba(16, 185, 129, 0.8)';
                uploadArea.querySelector('p').textContent = `Selected: ${fileName}`;
                uploadArea.querySelector('.upload-icon i').className = 'fas fa-file-pdf';
                uploadArea.querySelector('.upload-icon i').style.color = 'var(--success)';
            }
        });
    </script>
</body>
</html>"""

    # Enhanced Quiz Template
    quiz_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Generator - StudyGenie</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --accent: #06b6d4;
            --dark: #0f172a;
            --darker: #020617;
            --light: #f8fafc;
            --gray: #64748b;
            --success: #10b981;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, #1e1b4b 100%);
            color: var(--light);
            min-height: 100vh;
        }

        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }

        nav {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 20px;
            padding: 15px 0;
            margin-bottom: 30px;
            text-align: center;
        }

        nav a {
            color: var(--light);
            text-decoration: none;
            margin: 0 15px;
            padding: 8px 20px;
            background: rgba(99, 102, 241, 0.1);
            border-radius: 20px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: all 0.3s;
        }

        nav a:hover {
            background: rgba(99, 102, 241, 0.2);
            transform: translateY(-2px);
        }

        .hero {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 27, 75, 0.9));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }

        .hero h2 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }

        .quiz-form {
            max-width: 600px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: var(--light);
            font-size: 1.1rem;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 15px 20px;
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 15px;
            color: var(--light);
            font-size: 1rem;
            transition: all 0.3s;
        }

        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            margin: 20px 0;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
        }

        .quiz-results {
            margin-top: 40px;
            animation: fadeInUp 0.6s ease-out;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .quiz-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .quiz-header h3 {
            font-size: 1.8rem;
            color: var(--success);
            margin-bottom: 10px;
        }

        .question-item {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 25px;
            margin: 20px 0;
            border-radius: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .question-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(99, 102, 241, 0.2);
        }

        .question-number {
            position: absolute;
            top: 15px;
            right: 20px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-weight: 700;
            font-size: 0.9rem;
        }

        .question-text {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--light);
            line-height: 1.6;
            padding-right: 60px;
        }

        .question-type {
            background: rgba(6, 182, 212, 0.2);
            color: var(--accent);
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .answer-area {
            margin-top: 15px;
            padding: 15px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 10px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }

        .answer-area textarea {
            width: 100%;
            min-height: 80px;
            background: transparent;
            border: none;
            color: var(--light);
            resize: vertical;
            font-family: inherit;
            font-size: 1rem;
            line-height: 1.5;
        }

        .answer-area textarea::placeholder {
            color: var(--gray);
        }

        .answer-area textarea:focus {
            outline: none;
        }

        .quiz-actions {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            justify-content: center;
        }

        .btn-secondary {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            border: 1px solid rgba(99, 102, 241, 0.4);
            width: auto;
            padding: 12px 25px;
            font-size: 1rem;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(99, 102, 241, 0.3);
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .container { padding: 15px; }
            .hero { padding: 30px 25px; }
            .hero h2 { font-size: 2rem; }
            .quiz-actions { flex-direction: column; }
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
        </nav>

        <div class="hero">
            <h2><i class="fas fa-brain"></i> AI Quiz Generator</h2>
            <p style="text-align: center; color: var(--gray); font-size: 1.1rem; margin-bottom: 40px;">
                Create personalized practice questions instantly with artificial intelligence
            </p>

            <form id="quizForm" class="quiz-form">
                <div class="form-group">
                    <label for="topic"><i class="fas fa-book"></i> Study Topic</label>
                    <input type="text" id="topic" placeholder="e.g., Data Structures, Machine Learning, Thermodynamics" required>
                </div>

                <div class="form-group">
                    <label for="numQuestions"><i class="fas fa-list-ol"></i> Number of Questions</label>
                    <select id="numQuestions">
                        <option value="3">3 Questions (Quick Review)</option>
                        <option value="5" selected>5 Questions (Standard)</option>
                        <option value="8">8 Questions (Comprehensive)</option>
                        <option value="10">10 Questions (Deep Dive)</option>
                    </select>
                </div>

                <button type="submit" class="btn">
                    <i class="fas fa-magic"></i> Generate AI Quiz
                </button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI is crafting your personalized quiz... Please wait</p>
            </div>

            <div id="quizResults" class="quiz-results" style="display:none;">
                <div class="quiz-header">
                    <h3><i class="fas fa-check-circle"></i> Your AI-Generated Quiz</h3>
                    <p style="color: var(--gray);">Answer the questions below to test your knowledge</p>
                </div>
                <div id="questionsList"></div>
                <div class="quiz-actions">
                    <button onclick="printQuiz()" class="btn btn-secondary">
                        <i class="fas fa-print"></i> Print Quiz
                    </button>
                    <button onclick="generateNewQuiz()" class="btn btn-secondary">
                        <i class="fas fa-refresh"></i> Generate New
                    </button>
                    <button onclick="gradeQuiz()" class="btn">
                        <i class="fas fa-check"></i> Self-Grade
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('quizForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const topic = document.getElementById('topic').value;
            const numQuestions = document.getElementById('numQuestions').value;

            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('quizResults').style.display = 'none';

            try {
                const response = await fetch('/generate_quiz', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({topic, num_questions: parseInt(numQuestions)})
                });

                const data = await response.json();
                displayQuiz(data.questions);
            } catch (error) {
                console.error('Error:', error);
                alert('Error generating quiz: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });

        function displayQuiz(questions) {
            const questionsList = document.getElementById('questionsList');
            questionsList.innerHTML = '';

            questions.forEach((q, index) => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question-item';
                questionDiv.innerHTML = `
                    <div class="question-number">Q${q.id}</div>
                    <div class="question-text">${q.question}</div>
                    <div class="question-type">${q.type.replace('_', ' ')}</div>
                    <div class="answer-area">
                        <textarea placeholder="Write your answer here..." rows="3"></textarea>
                    </div>
                `;
                questionsList.appendChild(questionDiv);
            });

            document.getElementById('quizResults').style.display = 'block';

            // Animate questions appearance
            const questions_elements = document.querySelectorAll('.question-item');
            questions_elements.forEach((el, index) => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    el.style.transition = 'all 0.5s ease-out';
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, index * 150);
            });
        }

        function printQuiz() {
            window.print();
        }

        function generateNewQuiz() {
            document.getElementById('quizForm').dispatchEvent(new Event('submit'));
        }

        function gradeQuiz() {
            const answers = document.querySelectorAll('.answer-area textarea');
            let completed = 0;
            answers.forEach(answer => {
                if (answer.value.trim().length > 10) completed++;
            });

            const percentage = Math.round((completed / answers.length) * 100);
            alert(`Quiz Completion: ${percentage}%\n\nAnswered: ${completed}/${answers.length} questions\n\nKeep up the great work!`);
        }

        // Auto-save answers to localStorage
        document.addEventListener('change', function(e) {
            if (e.target.tagName === 'TEXTAREA') {
                const topic = document.getElementById('topic').value;
                const answers = Array.from(document.querySelectorAll('.answer-area textarea')).map(ta => ta.value);
                localStorage.setItem(`quiz_${topic}`, JSON.stringify(answers));
            }
        });
    </script>
</body>
</html>"""

    # Enhanced Schedule Template
    schedule_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Study Planner - StudyGenie</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --accent: #06b6d4;
            --dark: #0f172a;
            --darker: #020617;
            --light: #f8fafc;
            --gray: #64748b;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, #1e1b4b 100%);
            color: var(--light);
            min-height: 100vh;
        }

        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }

        nav {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 20px;
            padding: 15px 0;
            margin-bottom: 30px;
            text-align: center;
        }

        nav a {
            color: var(--light);
            text-decoration: none;
            margin: 0 15px;
            padding: 8px 20px;
            background: rgba(99, 102, 241, 0.1);
            border-radius: 20px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: all 0.3s;
        }

        nav a:hover {
            background: rgba(99, 102, 241, 0.2);
            transform: translateY(-2px);
        }

        .hero {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 27, 75, 0.9));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }

        .hero h2 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }

        .schedule-form {
            max-width: 600px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: var(--light);
            font-size: 1.1rem;
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 15px 20px;
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 15px;
            color: var(--light);
            font-size: 1rem;
            transition: all 0.3s;
            font-family: inherit;
        }

        .form-group textarea {
            min-height: 120px;
            resize: vertical;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            margin: 20px 0;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
        }

        .schedule-results {
            margin-top: 40px;
            animation: fadeInUp 0.6s ease-out;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .schedule-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .schedule-header h3 {
            font-size: 1.8rem;
            color: var(--success);
            margin-bottom: 10px;
        }

        .schedule-grid {
            display: grid;
            gap: 20px;
        }

        .schedule-item {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 25px;
            border-radius: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .schedule-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(99, 102, 241, 0.2);
        }

        .subject-name {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--light);
        }

        .priority-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .priority-high {
            background: linear-gradient(135deg, var(--danger), #dc2626);
            color: white;
        }

        .priority-medium {
            background: linear-gradient(135deg, var(--warning), #d97706);
            color: white;
        }

        .priority-normal {
            background: linear-gradient(135deg, var(--success), #059669);
            color: white;
        }

        .study-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }

        .stat-item {
            text-align: center;
            padding: 12px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 12px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--accent);
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--gray);
            margin-top: 2px;
        }

        .study-tips {
            margin-top: 15px;
            padding: 15px;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 12px;
            color: var(--light);
        }

        .study-tips::before {
            content: '💡 ';
            font-size: 1.2rem;
            margin-right: 8px;
        }

        .schedule-actions {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            justify-content: center;
        }

        .btn-secondary {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            border: 1px solid rgba(99, 102, 241, 0.4);
            width: auto;
            padding: 12px 25px;
            font-size: 1rem;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(99, 102, 241, 0.3);
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .container { padding: 15px; }
            .hero { padding: 30px 25px; }
            .hero h2 { font-size: 2rem; }
            .form-row { grid-template-columns: 1fr; }
            .schedule-actions { flex-direction: column; }
            .study-stats { grid-template-columns: repeat(2, 1fr); }
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
        </nav>

        <div class="hero">
            <h2><i class="fas fa-calendar-alt"></i> AI Study Planner</h2>
            <p style="text-align: center; color: var(--gray); font-size: 1.1rem; margin-bottom: 40px;">
                Create optimized study schedules powered by artificial intelligence
            </p>

            <form id="scheduleForm" class="schedule-form">
                <div class="form-group">
                    <label for="subjects"><i class="fas fa-book-open"></i> Your Subjects</label>
                    <textarea id="subjects" placeholder="Enter each subject on a new line:&#10;Data Structures & Algorithms&#10;Database Management Systems&#10;Computer Networks&#10;Operating Systems&#10;Machine Learning" required></textarea>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="examDate"><i class="fas fa-calendar-check"></i> Exam Date</label>
                        <input type="date" id="examDate" required>
                    </div>

                    <div class="form-group">
                        <label for="hoursPerDay"><i class="fas fa-clock"></i> Daily Study Hours</label>
                        <select id="hoursPerDay">
                            <option value="2">2 hours (Light)</option>
                            <option value="4" selected>4 hours (Moderate)</option>
                            <option value="6">6 hours (Intensive)</option>
                            <option value="8">8 hours (Extreme)</option>
                        </select>
                    </div>
                </div>

                <button type="submit" class="btn">
                    <i class="fas fa-magic"></i> Generate AI Schedule
                </button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI is optimizing your study schedule... Please wait</p>
            </div>

            <div id="scheduleResults" class="schedule-results" style="display:none;">
                <div class="schedule-header">
                    <h3><i class="fas fa-check-circle"></i> Your Optimized Study Plan</h3>
                    <p style="color: var(--gray);">Follow this AI-generated schedule for maximum efficiency</p>
                </div>
                <div id="scheduleList" class="schedule-grid"></div>
                <div class="schedule-actions">
                    <button onclick="downloadSchedule()" class="btn btn-secondary">
                        <i class="fas fa-download"></i> Download
                    </button>
                    <button onclick="printSchedule()" class="btn btn-secondary">
                        <i class="fas fa-print"></i> Print
                    </button>
                    <button onclick="shareSchedule()" class="btn btn-secondary">
                        <i class="fas fa-share"></i> Share
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Set minimum date to today
        document.getElementById('examDate').min = new Date().toISOString().split('T')[0];

        document.getElementById('scheduleForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const subjectsText = document.getElementById('subjects').value;
            const subjects = subjectsText.split('\n').filter(s => s.trim().length > 0);
            const examDate = document.getElementById('examDate').value;
            const hoursPerDay = parseInt(document.getElementById('hoursPerDay').value);

            if (subjects.length === 0) {
                alert('Please enter at least one subject');
                return;
            }

            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('scheduleResults').style.display = 'none';

            try {
                const response = await fetch('/generate_schedule', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({subjects, exam_date: examDate, hours_per_day: hoursPerDay})
                });

                const data = await response.json();
                displaySchedule(data.schedule);
            } catch (error) {
                console.error('Error:', error);
                alert('Error generating schedule: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });

        function displaySchedule(schedule) {
            const scheduleList = document.getElementById('scheduleList');

            if (schedule[0]?.error) {
                scheduleList.innerHTML = `<div style="color: var(--danger); text-align: center; padding: 20px;">Error: ${schedule[0].error}</div>`;
                document.getElementById('scheduleResults').style.display = 'block';
                return;
            }

            scheduleList.innerHTML = '';

            schedule.forEach((item, index) => {
                const scheduleItem = document.createElement('div');
                scheduleItem.className = 'schedule-item';

                const priorityClass = `priority-${item.priority.toLowerCase()}`;

                scheduleItem.innerHTML = `
                    <div class="priority-badge ${priorityClass}">${item.priority}</div>
                    <div class="subject-name">${item.subject}</div>
                    <div class="study-stats">
                        <div class="stat-item">
                            <div class="stat-number">${item.daily_hours}h</div>
                            <div class="stat-label">Daily</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${item.recommended_hours}h</div>
                            <div class="stat-label">Total</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${item.days_allocated}</div>
                            <div class="stat-label">Days</div>
                        </div>
                    </div>
                    <div class="study-tips">${item.study_tips}</div>
                `;

                scheduleList.appendChild(scheduleItem);
            });

            document.getElementById('scheduleResults').style.display = 'block';

            // Animate schedule items
            const items = document.querySelectorAll('.schedule-item');
            items.forEach((item, index) => {
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    item.style.transition = 'all 0.5s ease-out';
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, index * 150);
            });
        }

        function downloadSchedule() {
            const scheduleData = document.getElementById('scheduleList').innerText;
            const blob = new Blob([scheduleData], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'study-schedule.txt';
            a.click();
            window.URL.revokeObjectURL(url);
        }

        function printSchedule() {
            window.print();
        }

        function shareSchedule() {
            if (navigator.share) {
                const scheduleText = document.getElementById('scheduleList').innerText;
                navigator.share({
                    title: 'My AI Study Schedule',
                    text: scheduleText
                });
            } else {
                alert('Sharing not supported on this device');
            }
        }

        // Auto-save form data
        document.addEventListener('input', function(e) {
            if (e.target.form && e.target.form.id === 'scheduleForm') {
                const formData = new FormData(e.target.form);
                const data = Object.fromEntries(formData.entries());
                data.subjects = document.getElementById('subjects').value;
                localStorage.setItem('schedule_form', JSON.stringify(data));
            }
        });

        // Load saved form data
        window.addEventListener('load', function() {
            const saved = localStorage.getItem('schedule_form');
            if (saved) {
                const data = JSON.parse(saved);
                if (data.subjects) document.getElementById('subjects').value = data.subjects;
                if (data.examDate) document.getElementById('examDate').value = data.examDate;
                if (data.hoursPerDay) document.getElementById('hoursPerDay').value = data.hoursPerDay;
            }
        });
    </script>
</body>
</html>"""

    # Write all enhanced templates
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('templates/upload.html', 'w', encoding='utf-8') as f:
        f.write(upload_html)
    with open('templates/quiz.html', 'w', encoding='utf-8') as f:
        f.write(quiz_html)
    with open('templates/schedule.html', 'w', encoding='utf-8') as f:
        f.write(schedule_html)

create_enhanced_templates()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and file.filename.endswith('.pdf'):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            text = extract_text_from_pdf(filepath)
            summary = generate_simple_summary(text)

            return render_template('upload.html', summary=summary, filename=filename)

    return render_template('upload.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    topic = request.json.get('topic', '')
    num_questions = request.json.get('num_questions', 5)

    questions = generate_quiz_questions(topic, num_questions)
    return jsonify({'questions': questions})

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    subjects = data.get('subjects', [])
    exam_date = data.get('exam_date', '')
    hours_per_day = data.get('hours_per_day', 4)

    schedule = create_study_schedule(subjects, exam_date, hours_per_day)
    return jsonify({'schedule': schedule})

def extract_text_from_pdf(filepath):
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                if page_num < 3:
                    text += page.extract_text()
            return text[:1500]
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def generate_simple_summary(text):
    if len(text) < 100:
        return "Text too short to summarize. Please upload a longer document."

    sentences = text.replace('\n', ' ').split('. ')
    sentences = [s.strip() for s in sentences if len(s) > 20]

    summary_sentences = sentences[:3]

    key_terms = ['definition', 'theory', 'concept', 'principle', 'formula']
    for sentence in sentences:
        if any(term in sentence.lower() for term in key_terms) and len(summary_sentences) < 5:
            summary_sentences.append(sentence)

    summary = '. '.join(summary_sentences[:5]) + '.'
    return summary if len(summary) > 50 else "Summary: " + text[:300] + "..."

def generate_quiz_questions(topic, num_questions):
    question_templates = [
        f"What are the key concepts and fundamentals of {topic}?",
        f"Explain the significance and applications of {topic} in your field.",
        f"List and describe three important practical applications of {topic}.",
        f"How does {topic} connect to and influence other related concepts?",
        f"What are the main challenges and limitations in {topic}?",
        f"Describe the practical implementation and uses of {topic}.",
        f"What are the core principles and theoretical foundations of {topic}?",
        f"How would you approach solving a complex problem involving {topic}?"
    ]

    questions = []
    selected = random.sample(question_templates, min(num_questions, len(question_templates)))

    for i, template in enumerate(selected):
        questions.append({
            "id": i + 1,
            "question": template,
            "type": "short_answer" if i % 2 == 0 else "essay",
            "points": 5 if "short_answer" else 10
        })

    return questions

def create_study_schedule(subjects, exam_date, hours_per_day):
    try:
        exam_date_obj = datetime.strptime(exam_date, '%Y-%m-%d')
        days_until_exam = max(1, (exam_date_obj - datetime.now()).days)

        schedule = []
        total_hours_per_subject = max(1, (days_until_exam * hours_per_day) // len(subjects))

        for i, subject in enumerate(subjects):
            if i < len(subjects)//3:
                priority = "High"
            elif i < 2*len(subjects)//3:
                priority = "Medium"
            else:
                priority = "Normal"

            schedule.append({
                'subject': subject,
                'recommended_hours': total_hours_per_subject,
                'daily_hours': max(1, hours_per_day // len(subjects)),
                'priority': priority,
                'study_tips': get_enhanced_study_tips(subject),
                'days_allocated': days_until_exam
            })

        return schedule
    except Exception as e:
        return [{"error": f"Schedule generation failed: {str(e)}"}]

def get_enhanced_study_tips(subject):
    tips = {
        'mathematics': 'Focus on problem-solving techniques, practice numerical examples, and review fundamental theorems',
        'math': 'Focus on problem-solving techniques, practice numerical examples, and review fundamental theorems',
        'physics': 'Understand core concepts first, then practice derivations and numerical problems',
        'chemistry': 'Memorize key formulas, practice chemical equations, and understand reaction mechanisms',
        'computer science': 'Code regularly, understand algorithms deeply, and practice implementation',
        'programming': 'Code regularly, understand algorithms deeply, and practice implementation',
        'database': 'Practice SQL queries, understand normalization, and learn database design principles',
        'data structures': 'Implement each data structure, understand time complexities, and solve practice problems',
        'algorithms': 'Analyze time and space complexity, practice problem-solving, and understand algorithm design',
        'networks': 'Understand protocols, practice network configuration, and learn troubleshooting techniques',
        'operating systems': 'Study process management, memory allocation, and system call implementations',
        'machine learning': 'Understand mathematical foundations, implement algorithms, and work with real datasets',
        'engineering': 'Connect theory to practical applications, solve numerical problems, and understand design principles'
    }

    subject_lower = subject.lower()
    for key, tip in tips.items():
        if key in subject_lower:
            return tip

    return f"Create a structured study plan with regular revision and practice sessions for {subject}"

if __name__ == '__main__':
    print("🚀 Enhanced StudyGenie is starting...")
    print("🎨 Beautiful dark theme with animations loaded!")
    print("📱 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
