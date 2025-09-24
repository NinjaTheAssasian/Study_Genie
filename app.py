from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
import os
from datetime import datetime, timedelta
import random
import json
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'studygenie_ultimate_3d_2025'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create directories first
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_history():
    """Initialize session history with code sessions"""
    if 'history' not in session:
        session['history'] = {
            'summaries': [],
            'quizzes': [],
            'schedules': [],
            'code_sessions': []
        }

def create_enhanced_templates():
    """Create all enhanced templates with 3D animations"""
    
    # ENHANCED 3D INDEX TEMPLATE
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudyGenie - Ultimate 3D AI Study Assistant</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        :root {
            --primary: #6366f1; --secondary: #8b5cf6; --accent: #06b6d4; --success: #10b981;
            --warning: #f59e0b; --danger: #ef4444; --dark: #0f0f23; --darker: #05050f;
            --light: #f8fafc; --gray: #64748b; --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, #1a1a3a 100%);
            color: var(--light); min-height: 100vh; overflow-x: hidden; position: relative;
            perspective: 1000px;
        }
        
        /* 3D Animated Background */
        .bg-animation {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2;
            background: 
                radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 60%),
                radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.15) 0%, transparent 60%),
                radial-gradient(circle at 40% 80%, rgba(6, 182, 212, 0.12) 0%, transparent 60%);
            animation: backgroundPulse 20s ease-in-out infinite;
        }
        
        @keyframes backgroundPulse {
            0%, 100% { 
                transform: translateZ(0) scale(1) rotate(0deg);
                filter: blur(0px) hue-rotate(0deg);
            }
            25% { 
                transform: translateZ(50px) scale(1.1) rotate(1deg);
                filter: blur(2px) hue-rotate(30deg);
            }
            50% { 
                transform: translateZ(-30px) scale(0.95) rotate(-1deg);
                filter: blur(1px) hue-rotate(-20deg);
            }
            75% { 
                transform: translateZ(30px) scale(1.05) rotate(0.5deg);
                filter: blur(3px) hue-rotate(45deg);
            }
        }
        
        /* Floating 3D Particles */
        .floating-particles {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            pointer-events: none; perspective: 2000px;
        }
        
        .particle {
            position: absolute; background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%; opacity: 0.1; animation: float3D 25s ease-in-out infinite;
            transform-style: preserve-3d;
        }
        
        .particle:nth-child(1) { 
            width: 120px; height: 120px; top: 10%; left: 15%; 
            animation-delay: 0s; animation-duration: 20s;
        }
        .particle:nth-child(2) { 
            width: 80px; height: 80px; top: 60%; right: 10%; 
            animation-delay: -8s; animation-duration: 25s;
        }
        .particle:nth-child(3) { 
            width: 100px; height: 100px; bottom: 20%; left: 10%; 
            animation-delay: -15s; animation-duration: 30s;
        }
        
        @keyframes float3D {
            0%, 100% { 
                transform: translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
                opacity: 0.1;
            }
            25% { 
                transform: translate3d(30px, -40px, 100px) rotateX(90deg) rotateY(45deg) rotateZ(15deg);
                opacity: 0.2;
            }
            50% { 
                transform: translate3d(-20px, 20px, -80px) rotateX(180deg) rotateY(90deg) rotateZ(-20deg);
                opacity: 0.15;
            }
            75% { 
                transform: translate3d(40px, 30px, 60px) rotateX(270deg) rotateY(135deg) rotateZ(25deg);
                opacity: 0.25;
            }
        }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; position: relative; }
        
        /* Enhanced 3D Header */
        header {
            text-align: center; margin-bottom: 60px; padding: 60px 40px;
            background: var(--glass); backdrop-filter: blur(25px);
            border: 1px solid var(--glass-border); border-radius: 30px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative; overflow: hidden; transform-style: preserve-3d;
            animation: headerFloat 8s ease-in-out infinite;
        }
        
        @keyframes headerFloat {
            0%, 100% { transform: translateZ(0) rotateX(0deg) rotateY(0deg); }
            50% { transform: translateZ(20px) rotateX(2deg) rotateY(1deg); }
        }
        
        .logo {
            font-size: 4.8rem; font-weight: 900;
            background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
            background-size: 300% 300%; background-clip: text; -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; margin-bottom: 20px; position: relative;
            transform: perspective(1000px) rotateX(10deg);
            animation: logoGlow 6s ease-in-out infinite, gradientShift 8s ease-in-out infinite;
        }
        
        @keyframes logoGlow {
            0%, 100% { 
                transform: perspective(1000px) rotateX(10deg) translateY(0px) scale(1);
                filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.3));
            }
            50% { 
                transform: perspective(1000px) rotateX(15deg) translateY(-15px) scale(1.05);
                filter: drop-shadow(0 0 40px rgba(139, 92, 246, 0.5));
            }
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .logo::before {
            content: '🧞‍♂️'; position: absolute; top: -30px; left: -100px; 
            font-size: 6rem; animation: genieFloat 5s ease-in-out infinite;
            filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.4));
        }
        
        @keyframes genieFloat {
            0%, 100% { transform: translate3d(0, 0, 0) rotateZ(0deg) scale(1); }
            50% { transform: translate3d(-5px, -40px, -30px) rotateZ(-3deg) scale(0.95); }
        }
        
        /* Enhanced Navigation */
        nav {
            background: var(--glass); backdrop-filter: blur(30px);
            border: 1px solid var(--glass-border); border-radius: 25px;
            padding: 25px; margin-bottom: 60px; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            animation: navFloat 12s ease-in-out infinite;
        }
        
        @keyframes navFloat {
            0%, 100% { transform: translateZ(0) rotateX(0deg); }
            50% { transform: translateZ(10px) rotateX(1deg); }
        }
        
        nav ul { list-style: none; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }
        
        nav a {
            color: var(--light); text-decoration: none; padding: 18px 35px;
            border-radius: 20px; background: var(--glass); border: 1px solid var(--glass-border);
            font-weight: 600; font-size: 1.1rem; display: inline-block;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden; transform-style: preserve-3d;
        }
        
        nav a:hover {
            transform: translate3d(0, -12px, 30px) rotateX(10deg) rotateY(5deg) scale(1.08);
            box-shadow: 0 30px 60px rgba(99, 102, 241, 0.4), 0 0 50px rgba(99, 102, 241, 0.3);
            border-color: var(--primary);
        }
        
        nav a i { 
            margin-right: 8px; transition: all 0.3s ease;
        }
        
        nav a:hover i {
            transform: rotateY(360deg) scale(1.2);
            text-shadow: 0 0 15px currentColor;
        }
        
        /* Hero Section */
        .hero {
            background: var(--glass); backdrop-filter: blur(30px);
            border: 1px solid var(--glass-border); border-radius: 35px;
            padding: 100px 70px; box-shadow: 0 40px 100px rgba(0, 0, 0, 0.4);
            position: relative; overflow: hidden; transform-style: preserve-3d;
            animation: heroBreath 15s ease-in-out infinite;
        }
        
        @keyframes heroBreath {
            0%, 100% { transform: translateZ(0) scale(1); }
            50% { transform: translateZ(20px) scale(1.02); }
        }
        
        .hero-title {
            font-size: 4rem; font-weight: 900; text-align: center; margin-bottom: 40px;
            background: linear-gradient(135deg, var(--light), var(--accent), var(--primary));
            background-size: 200% 200%; background-clip: text; -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; transform: perspective(800px) rotateX(5deg);
            animation: titleWave 8s ease-in-out infinite;
        }
        
        @keyframes titleWave {
            0%, 100% { transform: perspective(800px) rotateX(5deg) translateY(0); }
            50% { transform: perspective(800px) rotateX(8deg) translateY(-10px); }
        }
        
        /* Feature Cards with 3D Effects */
        .features {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 50px; margin-top: 80px;
        }
        
        .feature-card {
            background: var(--glass); backdrop-filter: blur(25px);
            border: 1px solid var(--glass-border); border-radius: 30px;
            padding: 60px 45px; text-align: center;
            transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden; transform-style: preserve-3d;
            animation: cardFloat 20s ease-in-out infinite;
        }
        
        .feature-card:nth-child(1) { animation-delay: 0s; }
        .feature-card:nth-child(2) { animation-delay: -5s; }
        .feature-card:nth-child(3) { animation-delay: -10s; }
        .feature-card:nth-child(4) { animation-delay: -15s; }
        
        @keyframes cardFloat {
            0%, 100% { transform: translateZ(0) rotateX(0deg) rotateY(0deg); }
            25% { transform: translateZ(20px) rotateX(5deg) rotateY(2deg); }
            50% { transform: translateZ(-10px) rotateX(-3deg) rotateY(-1deg); }
            75% { transform: translateZ(15px) rotateX(4deg) rotateY(3deg); }
        }
        
        .feature-card:hover {
            transform: perspective(1000px) rotateX(15deg) rotateY(8deg) translateZ(50px) scale(1.05);
            box-shadow: 0 50px 100px rgba(0, 0, 0, 0.5), 0 0 80px rgba(99, 102, 241, 0.3);
            border-color: var(--primary);
        }
        
        .feature-icon {
            font-size: 5rem; margin-bottom: 30px; display: block;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: iconSpin 15s ease-in-out infinite; transform-style: preserve-3d;
        }
        
        @keyframes iconSpin {
            0%, 100% { 
                transform: rotateY(0deg) rotateX(0deg) scale(1);
                filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.3));
            }
            25% { 
                transform: rotateY(90deg) rotateX(10deg) scale(1.1);
                filter: drop-shadow(0 0 40px rgba(139, 92, 246, 0.5));
            }
            50% { 
                transform: rotateY(180deg) rotateX(0deg) scale(1.05);
                filter: drop-shadow(0 0 30px rgba(6, 182, 212, 0.4));
            }
            75% { 
                transform: rotateY(270deg) rotateX(-10deg) scale(1.15);
                filter: drop-shadow(0 0 50px rgba(99, 102, 241, 0.6));
            }
        }
        
        .feature-title {
            font-size: 1.6rem; font-weight: 800; margin-bottom: 20px;
            color: var(--light); text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
        }
        
        .feature-description {
            font-size: 1.1rem; line-height: 1.7; margin-bottom: 35px; opacity: 0.85;
        }
        
        /* Enhanced 3D Buttons */
        .btn {
            display: inline-block; 
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white; padding: 20px 50px; text-decoration: none;
            border-radius: 30px; font-weight: 700; font-size: 1.2rem;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden; border: none; cursor: pointer;
            transform-style: preserve-3d; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        }
        
        .btn:hover {
            transform: translateZ(20px) rotateX(5deg) scale(1.08);
            box-shadow: 0 25px 60px rgba(99, 102, 241, 0.5), 0 0 60px rgba(139, 92, 246, 0.4);
        }
        
        .btn i { margin-right: 10px; }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero { padding: 60px 40px; }
            .hero-title { font-size: 2.8rem; }
            .logo { font-size: 3.5rem; }
            .features { grid-template-columns: 1fr; gap: 30px; }
            nav ul { flex-direction: column; gap: 15px; }
            .feature-card:hover { 
                transform: translateZ(20px) rotateX(5deg) scale(1.03);
            }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    <div class="floating-particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    
    <div class="container">
        <header>
            <div class="logo">StudyGenie</div>
            <p style="font-size: 1.5rem; margin-bottom: 15px;">Ultimate AI-Powered Study Assistant</p>
            <p style="color: var(--accent); font-size: 1.1rem;">🤖 Enhanced with Real 3D Animations • 🏆 Built for AIGNITION 2025</p>
        </header>

        <nav>
            <ul>
                <li><a href="/"><i class="fas fa-home"></i> Home</a></li>
                <li><a href="/upload"><i class="fas fa-file-pdf"></i> Summarizer</a></li>
                <li><a href="/quiz"><i class="fas fa-brain"></i> Quiz</a></li>
                <li><a href="/schedule"><i class="fas fa-calendar"></i> Planner</a></li>
                <li><a href="/code"><i class="fas fa-code"></i> Code Helper</a></li>
                <li><a href="/history"><i class="fas fa-history"></i> History</a></li>
            </ul>
        </nav>

        <main>
            <div class="hero">
                <h2 class="hero-title">Transform Your Study Experience with Real 3D AI</h2>
                <p style="font-size: 1.4rem; text-align: center; margin-bottom: 60px; opacity: 0.9; max-width: 900px; margin-left: auto; margin-right: auto;">
                    Experience the future of education with StudyGenie Ultimate - featuring stunning real 3D animations, 
                    advanced AI capabilities, and immersive visual effects that revolutionize your learning journey.
                </p>

                <div class="features">
                    <div class="feature-card">
                        <div class="feature-icon">📚</div>
                        <h3 class="feature-title">AI Document Summarizer</h3>
                        <p class="feature-description">Upload PDFs and get intelligent, contextual summaries powered by advanced AI technology</p>
                        <a href="/upload" class="btn"><i class="fas fa-rocket"></i>Try Summarizer</a>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">🧠</div>
                        <h3 class="feature-title">Smart Quiz Generator</h3>
                        <p class="feature-description">Generate unlimited practice questions with varying difficulty levels</p>
                        <a href="/quiz" class="btn"><i class="fas fa-magic"></i>Create Quiz</a>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">📅</div>
                        <h3 class="feature-title">AI Study Planner</h3>
                        <p class="feature-description">Get personalized study schedules optimized for your learning pace</p>
                        <a href="/schedule" class="btn"><i class="fas fa-calendar-alt"></i>Plan Studies</a>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">💻</div>
                        <h3 class="feature-title">Code Helper Pro</h3>
                        <p class="feature-description">Get expert assistance with programming in multiple languages</p>
                        <a href="/code" class="btn"><i class="fas fa-code"></i>Code Help</a>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Enhanced 3D mouse parallax effect
        document.addEventListener('mousemove', function(e) {
            const particles = document.querySelectorAll('.particle');
            const cards = document.querySelectorAll('.feature-card');
            const header = document.querySelector('header');
            const nav = document.querySelector('nav');
            
            const x = (e.clientX / window.innerWidth) - 0.5;
            const y = (e.clientY / window.innerHeight) - 0.5;

            // Enhanced particle movement
            particles.forEach((particle, index) => {
                const speed = (index + 1) * 1.5;
                const rotateX = y * speed * 40;
                const rotateY = x * speed * 40;
                const translateZ = Math.sin(Date.now() * 0.001 + index) * 50;
                
                particle.style.transform = `
                    translate3d(${x * speed * 20}px, ${y * speed * 20}px, ${translateZ}px) 
                    rotateX(${rotateX}deg) 
                    rotateY(${rotateY}deg)
                `;
            });

            // 3D card tilt effect
            cards.forEach((card) => {
                const rect = card.getBoundingClientRect();
                const cardX = (e.clientX - rect.left - rect.width / 2) / rect.width;
                const cardY = (e.clientY - rect.top - rect.height / 2) / rect.height;
                
                if (Math.abs(cardX) < 1 && Math.abs(cardY) < 1) {
                    card.style.transform = `
                        perspective(1000px) 
                        rotateX(${cardY * 15}deg) 
                        rotateY(${cardX * 15}deg) 
                        translateZ(${Math.abs(cardX + cardY) * 30}px)
                    `;
                }
            });

            // Header 3D effect
            header.style.transform = `
                perspective(1000px) 
                rotateX(${y * 8}deg) 
                rotateY(${x * 8}deg) 
                translateZ(10px)
            `;

            // Nav 3D effect
            nav.style.transform = `
                perspective(1000px) 
                rotateX(${y * 5}deg) 
                rotateY(${x * 5}deg) 
                translateZ(5px)
            `;
        });
    </script>
</body>
</html>'''

    # ENHANCED 3D CODE HELPER TEMPLATE
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
#code helper template
    code_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Helper Pro - StudyGenie Ultimate 3D</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@300;400;500;600&display=swap');
        
        :root {
            --primary: #6366f1; --secondary: #8b5cf6; --accent: #06b6d4; --success: #10b981;
            --warning: #f59e0b; --danger: #ef4444; --dark: #0f0f23; --darker: #05050f;
            --light: #f8fafc; --gray: #64748b; --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, #1a1a3a 100%);
            color: var(--light); min-height: 100vh; position: relative; perspective: 1000px;
        }
        
        .bg-animation {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background: 
                radial-gradient(circle at 25% 25%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
            animation: bgFloat3D 20s ease-in-out infinite;
        }
        
        @keyframes bgFloat3D {
            0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg) scale(1); }
            33% { transform: translate3d(20px, -15px, 50px) rotate(1deg) scale(1.1); }
            66% { transform: translate3d(-15px, 20px, -30px) rotate(-1deg) scale(0.9); }
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        header {
            text-align: center; margin-bottom: 40px; padding: 50px;
            background: var(--glass); backdrop-filter: blur(30px);
            border: 1px solid var(--glass-border); border-radius: 30px;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4); position: relative;
            animation: headerFloat3D 10s ease-in-out infinite;
        }
        
        @keyframes headerFloat3D {
            0%, 100% { transform: translateZ(0) rotateX(0deg) rotateY(0deg); }
            50% { transform: translateZ(30px) rotateX(5deg) rotateY(2deg); }
        }
        
        .header-title {
            font-size: 3.5rem; font-weight: 900;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 20px; transform: perspective(500px) rotateX(8deg);
            animation: titlePulse3D 8s ease-in-out infinite;
        }
        
        @keyframes titlePulse3D {
            0%, 100% { 
                transform: perspective(500px) rotateX(8deg) scale(1);
                filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.3));
            }
            50% { 
                transform: perspective(500px) rotateX(12deg) scale(1.05);
                filter: drop-shadow(0 0 50px rgba(139, 92, 246, 0.5));
            }
        }
        
        nav {
            background: var(--glass); backdrop-filter: blur(30px);
            border: 1px solid var(--glass-border); border-radius: 25px;
            padding: 20px; margin-bottom: 40px; text-align: center;
            animation: navFloat3D 15s ease-in-out infinite;
        }
        
        @keyframes navFloat3D {
            0%, 100% { transform: translateZ(0) rotateX(0deg); }
            50% { transform: translateZ(15px) rotateX(2deg); }
        }
        
        nav a {
            color: var(--light); text-decoration: none; margin: 0 15px;
            padding: 15px 30px; background: var(--glass);
            border: 1px solid var(--glass-border); border-radius: 20px;
            display: inline-block; transition: all 0.5s ease; font-weight: 600;
        }
        
        nav a:hover {
            transform: translate3d(0, -10px, 25px) rotateX(10deg);
            box-shadow: 0 25px 50px rgba(99, 102, 241, 0.4);
            border-color: var(--primary);
        }
        
        .code-helper {
            background: var(--glass); backdrop-filter: blur(30px);
            border: 1px solid var(--glass-border); border-radius: 30px;
            padding: 60px; box-shadow: 0 40px 100px rgba(0, 0, 0, 0.4);
            position: relative; animation: codeHelperBreath 18s ease-in-out infinite;
        }
        
        @keyframes codeHelperBreath {
            0%, 100% { transform: translateZ(0) scale(1); }
            50% { transform: translateZ(20px) scale(1.01); }
        }
        
        .language-selector { margin-bottom: 50px; }
        
        .selector-title {
            font-size: 2rem; font-weight: 800; margin-bottom: 30px; text-align: center;
            background: linear-gradient(135deg, var(--accent), var(--primary));
            background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .language-cards {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px; margin-bottom: 40px;
        }
        
        .lang-card {
            background: var(--glass); border: 2px solid var(--glass-border);
            border-radius: 25px; padding: 40px 25px; text-align: center; cursor: pointer;
            transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden; transform-style: preserve-3d;
            animation: cardBob 12s ease-in-out infinite;
        }
        
        @keyframes cardBob {
            0%, 100% { transform: translateZ(0) rotateY(0deg); }
            25% { transform: translateZ(15px) rotateY(5deg); }
            50% { transform: translateZ(-10px) rotateY(0deg); }
            75% { transform: translateZ(20px) rotateY(-5deg); }
        }
        
        .lang-card.active, .lang-card:hover {
            transform: perspective(1000px) rotateX(15deg) rotateY(10deg) translateZ(40px) scale(1.08);
            border-color: var(--primary);
            box-shadow: 0 30px 80px rgba(99, 102, 241, 0.4), 0 0 60px rgba(139, 92, 246, 0.3);
        }
        
        .lang-icon { 
            font-size: 3.5rem; margin-bottom: 20px;
            animation: iconRotate 10s ease-in-out infinite;
        }
        
        @keyframes iconRotate {
            0%, 100% { transform: rotateY(0deg) scale(1); }
            50% { transform: rotateY(180deg) scale(1.05); }
        }
        
        .lang-name { font-weight: 800; font-size: 1.2rem; }
        
        .form-group { margin-bottom: 30px; }
        
        .form-label {
            display: block; margin-bottom: 15px; font-weight: 700; font-size: 1.1rem;
            background: linear-gradient(135deg, var(--accent), var(--light));
            background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .form-textarea {
            width: 100%; padding: 25px; background: rgba(15, 15, 35, 0.9);
            border: 2px solid var(--glass-border); border-radius: 20px;
            color: var(--light); font-size: 1.1rem;
            font-family: 'Fira Code', monospace; min-height: 180px; resize: vertical;
            transition: all 0.5s ease; backdrop-filter: blur(15px);
        }
        
        .form-textarea:focus {
            outline: none; border-color: var(--primary);
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
            transform: translateZ(10px);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white; padding: 25px 60px; border: none; border-radius: 30px;
            font-size: 1.3rem; font-weight: 800; cursor: pointer; width: 100%;
            transition: all 0.6s ease; position: relative;
            box-shadow: 0 15px 40px rgba(99, 102, 241, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateZ(25px) rotateX(5deg) scale(1.05);
            box-shadow: 0 30px 80px rgba(99, 102, 241, 0.5);
        }
        
        .results-section { 
            margin-top: 60px; display: none; 
            animation: resultsAppear 1s ease-in-out;
        }
        
        @keyframes resultsAppear {
            from { opacity: 0; transform: translate3d(0, 50px, -100px) rotateX(-15deg); }
            to { opacity: 1; transform: translate3d(0, 0, 0) rotateX(0deg); }
        }
        
        .results-title {
            font-size: 2.2rem; font-weight: 900; margin-bottom: 30px; text-align: center;
            background: linear-gradient(135deg, var(--success), var(--accent));
            background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .code-result {
            background: rgba(15, 15, 35, 0.95); border: 1px solid var(--glass-border);
            border-radius: 25px; padding: 35px; margin-bottom: 35px; backdrop-filter: blur(20px);
        }
        
        .result-header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;
        }
        
        .result-type { 
            font-weight: 700; font-size: 1.1rem;
            background: linear-gradient(135deg, var(--accent), var(--primary));
            background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .copy-btn {
            background: rgba(6, 182, 212, 0.2); border: 1px solid rgba(6, 182, 212, 0.5);
            color: var(--accent); padding: 10px 20px; border-radius: 15px; cursor: pointer;
            transition: all 0.4s ease;
        }
        
        .copy-btn:hover {
            background: rgba(6, 182, 212, 0.3); transform: translateZ(10px) scale(1.05);
        }
        
        .code-block {
            background: rgba(5, 5, 15, 0.95); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 30px; font-family: 'Fira Code', monospace;
            font-size: 1rem; line-height: 1.7; overflow-x: auto; white-space: pre-wrap;
        }
        
        .explanation {
            background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.4);
            border-radius: 20px; padding: 30px; margin-top: 25px; line-height: 1.8;
        }
        
        @media (max-width: 768px) {
            .code-helper { padding: 40px 30px; }
            .header-title { font-size: 2.5rem; }
            .language-cards { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="container">
        <header>
            <h1 class="header-title">💻 Code Helper Pro</h1>
            <p style="font-size: 1.3rem; margin-bottom: 15px;">AI-Powered Programming Assistant</p>
            <p style="opacity: 0.9;">Get expert help with coding in multiple languages with stunning 3D interface</p>
        </header>

        <nav>
            <a href="/"><i class="fas fa-home"></i> Home</a>
            <a href="/upload"><i class="fas fa-file-pdf"></i> Summarizer</a>
            <a href="/quiz"><i class="fas fa-brain"></i> Quiz</a>
            <a href="/schedule"><i class="fas fa-calendar"></i> Planner</a>
            <a href="/code"><i class="fas fa-code"></i> Code Helper</a>
            <a href="/history"><i class="fas fa-history"></i> History</a>
        </nav>

        <div class="code-helper">
            <div class="language-selector">
                <h2 class="selector-title">Choose Your Programming Language</h2>
                <div class="language-cards">
                    <div class="lang-card active" data-lang="python">
                        <div class="lang-icon">🐍</div>
                        <div class="lang-name">Python</div>
                    </div>
                    <div class="lang-card" data-lang="javascript">
                        <div class="lang-icon">🌐</div>
                        <div class="lang-name">JavaScript</div>
                    </div>
                    <div class="lang-card" data-lang="java">
                        <div class="lang-icon">☕</div>
                        <div class="lang-name">Java</div>
                    </div>
                    <div class="lang-card" data-lang="cpp">
                        <div class="lang-icon">⚡</div>
                        <div class="lang-name">C++</div>
                    </div>
                    <div class="lang-card" data-lang="html">
                        <div class="lang-icon">🌍</div>
                        <div class="lang-name">HTML/CSS</div>
                    </div>
                    <div class="lang-card" data-lang="sql">
                        <div class="lang-icon">🗄️</div>
                        <div class="lang-name">SQL</div>
                    </div>
                </div>
            </div>

            <form id="codeForm">
                <input type="hidden" id="selectedLanguage" value="python">
                
                <div class="form-group">
                    <label class="form-label">💬 Describe your coding problem or question:</label>
                    <textarea 
                        id="problemDescription" 
                        class="form-textarea" 
                        placeholder="Example: Create a function that finds the largest element in a list, or help me debug this code..."
                        required
                    ></textarea>
                </div>
                
                <div class="form-group">
                    <label class="form-label">📝 Paste your existing code (optional):</label>
                    <textarea 
                        id="existingCode" 
                        class="form-textarea" 
                        placeholder="Paste your current code here if you need help debugging or improving it..."
                        style="min-height: 220px;"
                    ></textarea>
                </div>
                
                <button type="submit" class="btn-primary">
                    <i class="fas fa-magic"></i> Get AI Code Help
                </button>
            </form>

            <div class="results-section" id="resultsSection">
                <h3 class="results-title">🚀 AI Code Solution & Expert Analysis</h3>
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>

    <script>
        let selectedLanguage = 'python';

        // Language selection
        document.querySelectorAll('.lang-card').forEach(card => {
            card.addEventListener('click', function() {
                document.querySelectorAll('.lang-card').forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                selectedLanguage = this.dataset.lang;
            });
        });

        // Form submission
        document.getElementById('codeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const problemDescription = document.getElementById('problemDescription').value;
            const existingCode = document.getElementById('existingCode').value;
            
            if (!problemDescription.trim()) {
                alert('Please describe your coding problem or question.');
                return;
            }

            // Generate sample solution
            setTimeout(() => {
                const solutions = {
                    python: `def solve_problem():
    """${problemDescription}"""
    # TODO: Implement your Python solution
    result = None
    return result

# Example usage
if __name__ == "__main__":
    result = solve_problem()
    print(f"Result: {result}")`,
                    
                    javascript: `// ${problemDescription}
function solveProblem(data) {
    // TODO: Implement your JavaScript solution
    let result = null;
    return result;
}

// Example usage
const result = solveProblem();
console.log('Result:', result);`,
                    
                    java: `public class Solution {
    // ${problemDescription}
    public Object solveProblem(Object data) {
        // TODO: Implement your Java solution
        return data;
    }
    
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println("Result: " + solution.solveProblem("test"));
    }
}`,
                    
                    cpp: `#include <iostream>
using namespace std;

// ${problemDescription}
class Solution {
public:
    auto solveProblem() {
        // TODO: Implement your C++ solution
        return nullptr;
    }
};

int main() {
    Solution solution;
    cout << "Result: " << solution.solveProblem() << endl;
    return 0;
}`,
                    
                    html: `<!DOCTYPE html>
<html>
<head>
    <title>${problemDescription}</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Your Solution</h1>
        <!-- TODO: Add your HTML content -->
    </div>
</body>
</html>`,
                    
                    sql: `-- ${problemDescription}
SELECT 
    column1,
    column2,
    COUNT(*) as count
FROM your_table
WHERE condition = 'value'
GROUP BY column1, column2
ORDER BY count DESC;`
                };
                
                const code = solutions[selectedLanguage] || solutions.python;
                const explanation = `This ${selectedLanguage} solution provides a template for: ${problemDescription}. Customize the implementation according to your specific requirements.`;
                
                displayResults(code, explanation);
            }, 1000);
        });

        function displayResults(code, explanation) {
            const resultsContent = document.getElementById('resultsContent');
            
            resultsContent.innerHTML = `
                <div class="code-result">
                    <div class="result-header">
                        <span class="result-type">💡 ${selectedLanguage.toUpperCase()} Code Solution</span>
                        <button class="copy-btn" onclick="copyToClipboard(\`${code.replace(/`/g, '\\`')}\`)">
                            <i class="fas fa-copy"></i> Copy
                        </button>
                    </div>
                    <div class="code-block"><code>${escapeHtml(code)}</code></div>
                </div>
                
                <div class="code-result">
                    <div class="result-header">
                        <span class="result-type">📚 Explanation</span>
                    </div>
                    <div class="explanation">${escapeHtml(explanation)}</div>
                </div>
            `;
            
            document.getElementById('resultsSection').style.display = 'block';
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target.closest('.copy-btn');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    btn.innerHTML = originalText;
                }, 2000);
            });
        }

        // 3D mouse effects
        document.addEventListener('mousemove', function(e) {
            const cards = document.querySelectorAll('.lang-card');
            const x = (e.clientX / window.innerWidth) - 0.5;
            const y = (e.clientY / window.innerHeight) - 0.5;

            cards.forEach((card, index) => {
                if (!card.matches(':hover')) {
                    const rotateX = y * 10;
                    const rotateY = x * 10;
                    
                    card.style.transform = `
                        perspective(1000px) 
                        rotateX(${rotateX}deg) 
                        rotateY(${rotateY}deg) 
                        translateZ(5px)
                    `;
                }
            });
        });
    </script>
</body>
</html>'''

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
    with open('templates/code.html','w',encoding='utf-8')as f:
        f.write(code_html)
create_enhanced_templates()
#routes
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
@app.route('/code')
def code():
    """Enhanced 3D Code Helper page"""
    init_history()
    return render_template('code.html')
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
    print("\n" + "="*70)
    print("🚀 STUDYGENIE ULTIMATE - REAL 3D EDITION STARTING...")
    print("="*70)
    print("✨ STUNNING NEW FEATURES:")
    print("   • 🎭 REAL 3D animations with depth and perspective")
    print("   • 🎨 Advanced glassmorphism with backdrop blur effects")
    print("   • 💫 Floating particles with 3D transformations")
    print("   • 🌈 Dynamic gradient animations and color shifting")
    print("   • 💻 Complete Code Helper Pro with 6 programming languages")
    print("   • 🎪 Interactive mouse parallax effects")
    print("   • 📱 Responsive design with mobile optimization")
    print("   • ⚡ Enhanced performance and smooth transitions")
    print("\n📱 Access your 3D StudyGenie at: http://localhost:5000")
    print("🎯 Features: Summarizer • Quiz • Planner • CODE HELPER • History")
    print("🏆 Ready to dominate AIGNITION 2025 with REAL 3D effects!\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')