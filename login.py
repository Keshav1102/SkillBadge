import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
import json
import os

# Custom CSS for the login page
st.markdown("""
    <style>
    /* Modern Design System */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');
    :root {
        --primary-gradient: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        --accent-gradient: linear-gradient(135deg, #FFD93D 0%, #FF6B6B 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-blur: blur(20px);
        --card-bg: rgba(255, 255, 255, 0.05);
        --border-glass: 1px solid rgba(255, 255, 255, 0.2);
        --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        --radius: 30px;
        --font: 'Montserrat', sans-serif;
        --text-light: #ffffff;
        --text-dark: #1a1a1a;
    }

    /* Animated Background */
    .animated-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating Particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }

    .particle {
        position: absolute;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        pointer-events: none;
        animation: float-up 20s linear infinite;
    }

    @keyframes float-up {
        0% {
            transform: translateY(100vh) scale(0);
            opacity: 0;
        }
        50% {
            opacity: 0.8;
        }
        100% {
            transform: translateY(-100px) scale(1);
            opacity: 0;
        }
    }

    /* Main Container */
    .login-container {
        background: var(--glass-bg);
        backdrop-filter: var(--glass-blur);
        border-radius: var(--radius);
        padding: 3rem;
        box-shadow: var(--shadow);
        border: var(--border-glass);
        max-width: 800px;
        margin: 2rem auto;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
        animation: container-float 6s ease-in-out infinite;
    }

    @keyframes container-float {
        0%, 100% { transform: translateY(0) rotateX(0) rotateY(0); }
        25% { transform: translateY(-10px) rotateX(2deg) rotateY(2deg); }
        75% { transform: translateY(10px) rotateX(-2deg) rotateY(-2deg); }
    }

    .login-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: var(--primary-gradient);
        opacity: 0.1;
        animation: rotate 20s linear infinite;
        z-index: -1;
    }

    /* Title Animation */
    .login-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: title-glow 2s ease-in-out infinite;
    }

    @keyframes title-glow {
        0%, 100% { text-shadow: 0 0 20px rgba(255, 255, 255, 0.5); }
        50% { text-shadow: 0 0 30px rgba(255, 255, 255, 0.8); }
    }

    /* Enhanced Button Styles */
    .stButton>button {
        width: 100%;
        background: var(--primary-gradient);
        color: var(--text-light);
        border: none;
        padding: 1.2rem;
        border-radius: var(--radius);
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transition: 0.5s;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }

    .stButton>button:hover::before {
        left: 100%;
    }

    /* Enhanced Input Fields */
    .stTextInput>div>div>input {
        background: var(--card-bg);
        border: var(--border-glass);
        border-radius: var(--radius);
        padding: 1.2rem;
        font-size: 1.1rem;
        color: var(--text-light);
        transition: all 0.3s ease;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stTextInput>div>div>input:focus {
        border-color: #4ECDC4;
        box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.3);
        transform: translateY(-2px);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        padding: 1rem;
        background: var(--card-bg);
        border-radius: var(--radius);
        margin: 2rem 0;
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-light);
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 2rem;
        border-radius: var(--radius);
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: var(--text-light);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    /* Message Styling */
    .success-message, .error-message {
        padding: 1.2rem;
        border-radius: var(--radius);
        margin: 1rem 0;
        backdrop-filter: var(--glass-blur);
        animation: message-slide 0.5s ease-out;
    }

    .success-message {
        background: rgba(46, 213, 115, 0.1);
        border: 1px solid rgba(46, 213, 115, 0.2);
        color: #2ed573;
    }

    .error-message {
        background: rgba(255, 71, 87, 0.1);
        border: 1px solid rgba(255, 71, 87, 0.2);
        color: #ff4757;
    }

    @keyframes message-slide {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .login-container {
            margin: 1rem;
            padding: 2rem;
        }
        .login-title {
            font-size: 2.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        if not os.path.exists("firebase_config.json"):
            st.error("""
            Firebase configuration file is missing! Please follow these steps:
            1. Go to the Firebase Console (https://console.firebase.google.com/)
            2. Select your project
            3. Go to Project Settings > Service Accounts
            4. Click 'Generate New Private Key'
            5. Save the downloaded file as 'firebase_config.json' in your project directory
            """)
            st.stop()
        
        cred = credentials.Certificate("firebase_config.json")
        firebase_admin.initialize_app(cred)
        st.success("Firebase initialized successfully!")
    except Exception as e:
        st.error(f"""
        Error initializing Firebase: {str(e)}
        
        Please make sure:
        1. You have downloaded the service account key from Firebase Console
        2. The file is named 'firebase_config.json'
        3. The file is in the correct directory
        4. The file contains valid JSON with all required fields
        """)
        st.stop()

# Initialize Firestore
try:
    db = firestore.client()
except Exception as e:
    if "SERVICE_DISABLED" in str(e):
        st.error("""
        Cloud Firestore API is not enabled! Please follow these steps:
        1. Go to the Firebase Console (https://console.firebase.google.com/)
        2. Select your project
        3. Click on 'Firestore Database' in the left sidebar
        4. Click 'Create Database'
        5. Choose your preferred location
        6. Start in production mode or test mode
        
        After creating the database, wait a few minutes for the changes to propagate.
        """)
    else:
        st.error(f"Error connecting to Firestore: {str(e)}")
    st.stop()

def show_login_page():
    # Add animated background
    st.markdown('<div class="animated-background"></div>', unsafe_allow_html=True)
    
    # Add floating particles
    st.markdown("""
        <div class="particles">
            <script>
                function createParticle() {
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.width = Math.random() * 10 + 5 + 'px';
                    particle.style.height = particle.style.width;
                    particle.style.left = Math.random() * 100 + 'vw';
                    particle.style.animationDuration = Math.random() * 20 + 10 + 's';
                    document.querySelector('.particles').appendChild(particle);
                    setTimeout(() => particle.remove(), 30000);
                }
                setInterval(createParticle, 300);
            </script>
        </div>
    """, unsafe_allow_html=True)
    
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Title and subtitle
        st.markdown('<h1 class="login-title">Welcome to MindForge</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Your AI-Powered Career Guidance Platform</p>', unsafe_allow_html=True)
        
        # Create tabs for Login and Register
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.markdown('<h2 style="text-align: center; color: var(--text-light);">Login</h2>', unsafe_allow_html=True)
            email = st.text_input("Email", key="login_email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            if st.button("Login", key="login_button"):
                try:
                    # Sign in with email and password
                    user = auth.get_user_by_email(email)
                    # Store user info in session state
                    st.session_state.user = {
                        "email": email,
                        "uid": user.uid
                    }
                    st.markdown('<div class="success-message">Login successful! Redirecting...</div>', unsafe_allow_html=True)
                    st.rerun()
                except Exception as e:
                    st.markdown(f'<div class="error-message">Login failed: {str(e)}</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<h2 style="text-align: center; color: var(--text-light);">Register</h2>', unsafe_allow_html=True)
            reg_email = st.text_input("Email", key="reg_email", placeholder="Enter your email")
            reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")
            
            if st.button("Register", key="register_button"):
                if reg_password != confirm_password:
                    st.markdown('<div class="error-message">Passwords do not match!</div>', unsafe_allow_html=True)
                else:
                    try:
                        # Create user with email and password
                        user = auth.create_user(
                            email=reg_email,
                            password=reg_password
                        )
                        # Create user document in Firestore
                        db.collection('users').document(user.uid).set({
                            'email': reg_email,
                            'created_at': firestore.SERVER_TIMESTAMP
                        })
                        st.markdown('<div class="success-message">Registration successful! Please login.</div>', unsafe_allow_html=True)
                    except Exception as e:
                        if "SERVICE_DISABLED" in str(e):
                            st.markdown("""
                            <div class="error-message">
                            Cloud Firestore API is not enabled! Please follow these steps:
                            1. Go to the Firebase Console (https://console.firebase.google.com/)
                            2. Select your project
                            3. Click on 'Firestore Database' in the left sidebar
                            4. Click 'Create Database'
                            5. Choose your preferred location
                            6. Start in production mode or test mode
                            
                            After creating the database, wait a few minutes for the changes to propagate.
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="error-message">Registration failed: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    if 'user' in st.session_state:
        del st.session_state.user
    st.rerun() 