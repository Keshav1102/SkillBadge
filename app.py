import streamlit as st
# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="MindForge - Career Guidance Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


import pandas as pd
import plotly.express as px
from PIL import Image
import numpy as np
from login import show_login_page, logout

# Initialize session state for authentication
if 'user' not in st.session_state:
    st.session_state.user = None

# Show login page if user is not authenticated
if not st.session_state.user:
    show_login_page()
    st.stop()

# Initialize session state for page navigation if not exists
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Initialize session state for tasks if not exists
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"title": "Complete Assessment", "due": "Today", "completed": False},
        {"title": "Update Profile", "due": "Tomorrow", "completed": False}
    ]

def add_task(title, due_date):
    st.session_state.tasks.append({"title": title, "due": due_date, "completed": False})

def toggle_task(index):
    st.session_state.tasks[index]["completed"] = not st.session_state.tasks[index]["completed"]

def delete_task(index):
    st.session_state.tasks.pop(index)

# Custom component for navigation
components = st.markdown("""
    <script>
    // Create a custom event handler
    window.addEventListener('nav_change', function(e) {
        // Update the session state
        window.parent.stStreamlitPyObject.setComponentValue({
            'page': e.detail.page
        });
    });
    </script>
""", unsafe_allow_html=True)

# Custom CSS with responsive design
# ...existing code...
st.markdown("""
    <style>
    /* Glassmorphism + Neumorphism + Vibrant Gradients */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    :root {
        --primary-gradient: linear-gradient(135deg, #6D5BFF 0%, #46C9E5 100%);
        --accent-gradient: linear-gradient(135deg, #FF6B6B 0%, #FFD93D 100%);
        --glass-bg: rgba(34, 40, 49, 0.75);
        --glass-blur: blur(18px);
        --card-bg: rgba(255,255,255,0.10);
        --border-glass: 1.5px solid rgba(255,255,255,0.25);
        --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.25);
        --radius: 22px;
        --font: 'Montserrat', 'Segoe UI', 'Roboto', Arial, sans-serif;
        --text-light: #f7f7fa;
        --text-dark: #22223b;
        --sidebar-width: 320px;
    }
    html, body, [class*="css"] {
        font-family: var(--font) !important;
        background: linear-gradient(120deg, #232526 0%, #414345 100%);
        color: var(--text-light);
    }
    .main {
        padding: 0 var(--spacing-unit);
        max-width: 1200px;
        margin: 0 auto;
    }
    /* Glassy sidebar */
    section[data-testid="stSidebar"] {
        background: var(--glass-bg) !important;
        backdrop-filter: var(--glass-blur);
        border-right: var(--border-glass);
        box-shadow: var(--shadow);
        min-width: var(--sidebar-width);
        max-width: var(--sidebar-width);
    }
    /* Profile image with neon ring */
    .profile-image {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        border: 4px solid #FFD93D;
        box-shadow: 0 0 0 6px #6D5BFF55, 0 4px 24px #0008;
        margin: 0 auto 1rem auto;
        display: block;
        background: var(--card-bg);
    }
    /* Neumorphic buttons */
    .stButton>button {
        width: 100%;
        background: var(--primary-gradient);
        color: #fff;
        border-radius: var(--radius);
        border: none;
        padding: 0.8rem 1.4rem;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 4px 4px 16px #23252655, -4px -4px 16px #6D5BFF33;
        transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
        letter-spacing: 0.03em;
    }
    .stButton>button:hover {
        background: var(--accent-gradient);
        color: #232526;
        transform: translateY(-2px) scale(1.04);
        box-shadow: 0 8px 32px #FFD93D33;
    }
    /* Glassy cards */
    .feature-card, .stat-box, .testimonial-card {
        background: var(--card-bg);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        border: var(--border-glass);
        backdrop-filter: var(--glass-blur);
        padding: clamp(1.2rem, 3vw, 2rem);
        margin: 0.7rem 0;
        transition: box-shadow 0.2s, border 0.2s;
    }
    .feature-card:hover, .stat-box:hover, .testimonial-card:hover {
        border: 2px solid #FFD93D;
        box-shadow: 0 12px 36px #FFD93D33;
    }
    /* Stat boxes with gradient border */
    .stat-box {
        text-align: center;
        border: 2px solid transparent;
        background: linear-gradient(var(--card-bg), var(--card-bg)) padding-box,
                    var(--primary-gradient) border-box;
    }
    /* Navigation links with glassy effect */
    .nav-link {
        padding: 0.85rem 1.3rem;
        margin: 0.5rem 0;
        border-radius: var(--radius);
        background: var(--card-bg);
        color: #FFD93D;
        font-weight: 700;
        display: flex;
        align-items: center;
        font-size: 1.05rem;
        box-shadow: var(--shadow);
        transition: background 0.2s, color 0.2s, border 0.2s;
        text-decoration: none;
        border: 2px solid transparent;
        letter-spacing: 0.02em;
    }
    .nav-link.active, .nav-link:hover {
        background: var(--primary-gradient);
        color: #fff;
        border: 2px solid #FFD93D;
    }
    .nav-link .notification-badge {
        background: #FF6B6B;
        color: #fff;
        padding: 0.2rem 0.7rem;
        border-radius: 12px;
        font-size: 0.85rem;
        margin-left: auto;
        font-weight: 700;
        box-shadow: 0 2px 8px #FF6B6B44;
    }
    /* Testimonials with glass border */
    .testimonial-card {
        border-left: 6px solid #FFD93D;
        font-style: italic;
        background: var(--glass-bg);
        color: #FFD93D;
    }
    /* Responsive grid with glassy cards */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: var(--spacing-unit);
        padding: var(--spacing-unit) 0;
    }
    /* Progress ring (neon) */
    .progress-ring {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: conic-gradient(#FFD93D 75%, #232526 0 100%);
        margin: 1.5rem auto 1rem auto;
        position: relative;
        box-shadow: 0 0 24px #FFD93D88, 0 2px 8px #0008;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .progress-ring h4, .progress-ring small {
        color: #FFD93D !important;
        text-shadow: 0 2px 8px #FFD93D44;
    }
    /* Misc spacing */
    .mt-responsive { margin-top: clamp(1rem, 3vw, 2rem); }
    .mb-responsive { margin-bottom: clamp(1rem, 3vw, 2rem); }
    .p-responsive { padding: clamp(1rem, 3vw, 2rem); }
    /* Custom highlight */
    .highlight {
        background: var(--accent-gradient);
        color: #232526;
        border-radius: 8px;
        padding: 0.1em 0.5em;
        box-shadow: 0 2px 8px #FFD93D44;
    }
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: #232526;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6D5BFF 0%, #FFD93D 100%);
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)
# ...existing code...
# Sidebar
with st.sidebar:
    # Profile Section
    st.markdown("""
        <div class='profile-section'>
            <img src='https://img.freepik.com/free-vector/businessman-character-avatar-isolated_24877-60111.jpg' 
                 class='profile-image'>
            <h3 style='margin-top: 1rem;'>Welcome {email}!</h3>
            <p style='color: #666;'>Your Career Journey Awaits</p>
        </div>
    """.format(email=st.session_state.user["email"]), unsafe_allow_html=True)
    
    # Logout button
    if st.button("Logout"):
        logout()
        st.stop()
    
    # Progress Ring
    st.markdown("""
        <div class='progress-ring'>
            <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);'>
                <h4 style='color: #FF4B4B; margin: 0;'>75%</h4>
                <small>Profile Complete</small>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Menu
    st.markdown("<h4 class='sidebar-title'>Navigation</h4>", unsafe_allow_html=True)
    
    # Create navigation links with icons and notifications
    nav_items = {
        "Home": {"icon": "🏠", "notifications": 0},
        "Career Assessment": {"icon": "📋", "notifications": 2},
        "Career Explorer": {"icon": "🔍", "notifications": 0},
        "Resources": {"icon": "📚", "notifications": 5},
        "Personal Dashboard": {"icon": "📊", "notifications": 1}
    }
    
    for nav_item, details in nav_items.items():
        is_active = st.session_state.page == nav_item
        
        # Add the functional button with icon
        if st.button(
            f"{details['icon']} {nav_item}",
            key=f"nav_{nav_item}",
            help=f"Navigate to {nav_item}",
            type="primary" if is_active else "secondary",
            use_container_width=True
        ):
            st.session_state.page = nav_item
    
    # Quick Stats
    st.markdown("---")
    st.markdown("<h4 class='sidebar-title'>Quick Stats</h4>", unsafe_allow_html=True)
    
    # Create two columns for stats
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.markdown("""
            <div style='text-align: center;'>
                <h4 style='color: #FF4B4B; margin: 0;'>5</h4>
                <small>Assessments</small>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
            <div style='text-align: center;'>
                <h4 style='color: #FF4B4B; margin: 0;'>12</h4>
                <small>Resources</small>
            </div>
        """, unsafe_allow_html=True)
    
    # Upcoming Tasks
    st.markdown("---")
    st.markdown("<h4 class='sidebar-title'>Upcoming Tasks</h4>", unsafe_allow_html=True)
    
    # Add new task
    with st.expander("➕ Add New Task"):
        task_title = st.text_input("Task Title", key="new_task_title")
        task_due = st.selectbox(
            "Due Date",
            ["Today", "Tomorrow", "This Week", "Next Week", "Custom"],
            key="new_task_due"
        )
        
        if task_due == "Custom":
            task_due = st.date_input("Select Date", key="custom_date")
            task_due = task_due.strftime("%Y-%m-%d")
        
        if st.button("Add Task"):
            if task_title:  # Only add if title is not empty
                add_task(task_title, task_due)
                # Clear the input
                st.session_state.new_task_title = ""
    
    # Display tasks
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([1, 8, 1])
        
        with col1:
            if st.checkbox("", task["completed"], key=f"task_{i}"):
                toggle_task(i)
        
        with col2:
            title_style = "text-decoration: line-through;" if task["completed"] else ""
            st.markdown(f"""
                <div style='padding: 0.5rem; background-color: white; border-radius: 5px; margin: 0.5rem 0;'>
                    <small style='color: #666;'>{task['due']}</small>
                    <p style='margin: 0; {title_style}'>{task['title']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("🗑️", key=f"delete_task_{i}"):
                delete_task(i)
                st.experimental_rerun()
    
    # Footer
    st.markdown("""
        <div class='sidebar-footer'>
            <small style='color: #666;'>Need Help?</small>
            <br>
            <a href='#' style='color: #FF4B4B; text-decoration: none;'>Contact Support</a>
        </div>
    """, unsafe_allow_html=True)

# Main content with responsive layouts
if st.session_state.page == "Home":
    # Hero Section with responsive design
    st.markdown("""
        <div style='text-align: center; padding: clamp(1rem, 5vw, 3rem) 0;'>
            <h1 style='font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem;'>
                Welcome to <span class='highlight'>MindForge</span> 🚀
            </h1>
            <p style='font-size: clamp(1rem, 2vw, 1.2rem); color: #666; margin-bottom: 2rem;'>
                Your AI-Powered Career Guidance Companion
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Responsive statistics grid
    st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
    for stat in [
        {"number": "10K+", "label": "Students Guided"},
        {"number": "500+", "label": "Career Paths"},
        {"number": "95%", "label": "Success Rate"},
        {"number": "24/7", "label": "AI Support"}
    ]:
        st.markdown(f"""
            <div class='stat-box'>
                <h2 style='color: var(--primary-color); font-size: clamp(1.5rem, 3vw, 2rem);'>
                    {stat['number']}
                </h2>
                <p style='color: var(--text-color); font-size: clamp(1.5rem, 0, 2rem);'>{stat['label']}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Interactive Demo Section with responsive layout
    st.markdown("---")
    cols = st.columns([2, 1])
    
    with cols[0]:
        st.markdown("### Try Our Quick Career Match! 🎯")
        interest_areas = st.multiselect(
            "Select your areas of interest:",
            ["Technology", "Science", "Arts", "Business", "Healthcare", "Education"],
            max_selections=3
        )
        
        skill_level = st.select_slider(
            "Rate your technical skills:",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
        
        preferred_work = st.radio(
            "Preferred work environment:",
            ["Remote", "Office", "Hybrid", "Field Work"]
        )

    with cols[1]:
        st.image("https://img.freepik.com/free-photo/thinking-man-with-suit_1154-106.jpg?ga=GA1.1.1303681271.1747159330&semt=ais_hybrid&w=740",
                 use_column_width=True)

    # Features grid with responsive cards
    st.markdown("### How MindForge Helps You 🌟")
    st.markdown("<div class='grid-container'>", unsafe_allow_html=True)
    
    features = [
        {
            "icon": "🎯",
            "title": "Career Assessment",
            "description": "Discover careers that match your interests and skills",
            "metric": "20 minutes to complete"
        },
        {
            "icon": "🔍",
            "title": "Career Explorer",
            "description": "Explore different career paths and prospects",
            "metric": "500+ career paths"
        },
        {
            "icon": "📚",
            "title": "Learning Resources",
            "description": "Access curated materials for your career path",
            "metric": "1000+ resources"
        }
    ]
    
    for feature in features:
        st.markdown(f"""
            <div class='feature-card'>
                <h3 style='color: #FF4B4B;'>{feature['icon']} {feature['title']}</h3>
                <p style='color: #666;'>{feature['description']}</p>
                <small style='color: var(--primary-color);'>{feature['metric']}</small>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Responsive testimonials
    st.markdown("### Success Stories 💫")
    testimonial_cols = st.columns(2)
    
    testimonials = [
        {
            "quote": "MindForge helped me discover my passion for data science. Now I'm working at my dream company!",
            "author": "Sarah P., Data Scientist"
        },
        {
            "quote": "The career guidance I received was invaluable. It helped me make an informed decision about my future.",
            "author": "James R., Software Engineer"
        }
    ]
    
    for i, testimonial in enumerate(testimonials):
        with testimonial_cols[i]:
            st.markdown(f"""
                <div class='testimonial-card'>
                    <p style='color: #666;font-style: italic;'>{testimonial["quote"]}</p>
                    <p style='color: #666;'>- {testimonial["author"]}</p>
                </div>
            """, unsafe_allow_html=True)

    # Call to Action
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h2>Ready to Start Your Journey? 🚀</h2>
            <p style='font-size: 1.2rem; color: #666; margin: 1rem 0;'>
                Join thousands of students who have found their perfect career path with MindForge
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
    with cta_col2:
        if st.button("Begin Your Career Journey", key="home_cta"):
            st.session_state.page = "Career Assessment"

elif st.session_state.page == "Career Assessment":
    st.title("Career Assessment 📝")
    
    # Personal Information
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=13, max_value=100)
    with col2:
        education = st.selectbox("Current Education Level", 
            ["High School", "Undergraduate", "Graduate", "Other"])
        location = st.text_input("Location")

    # Interest Assessment
    st.header("Interest Assessment")
    st.write("Rate your interest in the following areas (1-5):")
    
    interests = {
        "Technology": st.slider("Technology & Computing", 1, 5, 3),
        "Science": st.slider("Science & Research", 1, 5, 3),
        "Arts": st.slider("Arts & Creativity", 1, 5, 3),
        "Business": st.slider("Business & Management", 1, 5, 3),
        "Social": st.slider("Social Services & Teaching", 1, 5, 3)
    }
    
    if st.button("Generate Career Recommendations"):
        st.success("Based on your responses, here are some recommended career paths:")
        # Placeholder for recommendation logic
        st.write("1. Data Science & Analytics")
        st.write("2. Digital Marketing")
        st.write("3. Educational Technology")
        st.write("4. Healthcare Administration")
        st.write("5. Creative Design")

elif st.session_state.page == "Career Explorer":
    st.title("Career Explorer 🔍")
    
    # Career Categories
    categories = ["Technology", "Healthcare", "Business", "Education", "Creative Arts"]
    selected_category = st.selectbox("Select Career Category", categories)
    
    # Career Details (Placeholder data)
    careers = {
        "Technology": ["Software Developer", "Data Scientist", "Cybersecurity Analyst"],
        "Healthcare": ["Nurse Practitioner", "Medical Researcher", "Healthcare Administrator"],
        "Business": ["Financial Analyst", "Marketing Manager", "Entrepreneur"],
        "Education": ["Teacher", "Educational Consultant", "Instructional Designer"],
        "Creative Arts": ["Graphic Designer", "Content Creator", "UX Designer"]
    }
    
    selected_career = st.selectbox("Select Career", careers[selected_category])
    
    # Display career information
    st.header(f"About: {selected_career}")
    st.write("Career overview and detailed information would appear here...")
    
    # Skills Required
    st.subheader("Required Skills")
    st.write("Key skills for this career path...")
    
    # Job Market Trends
    st.subheader("Job Market Trends")
    # Placeholder chart
    data = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024],
        'Demand': [100, 120, 150, 180, 220]
    })
    fig = px.line(data, x='Year', y='Demand', title='Job Market Demand Trend')
    st.plotly_chart(fig)

elif st.session_state.page == "Resources":
    st.title("Learning Resources 📚")
    
    # Resource Categories
    st.header("Educational Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Online Courses")
        st.write("- Coursera")
        st.write("- edX")
        st.write("- Udemy")
        
        st.subheader("Certification Programs")
        st.write("- Professional Certifications")
        st.write("- Industry-specific Training")
        
    with col2:
        st.subheader("Career Development")
        st.write("- Resume Writing")
        st.write("- Interview Preparation")
        st.write("- Networking Tips")

elif st.session_state.page == "Personal Dashboard":
    st.title("Personal Dashboard 📊")
    
    # Profile Summary
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://img.freepik.com/free-vector/businessman-character-avatar-isolated_24877-60111.jpg", 
                 width=200, caption="Profile Picture")
    with col2:
        st.subheader("Welcome back, User! 👋")
        st.write("Last login: Today at 10:00 AM")
        st.write("Career Path: Technology & Computing")
        st.write("Completed Assessments: 3/5")
    
    # Quick Actions
    st.markdown("---")
    quick_actions_col1, quick_actions_col2, quick_actions_col3 = st.columns(3)
    with quick_actions_col1:
        if st.button("📝 Take New Assessment"):
            st.session_state.page = "Career Assessment"
    with quick_actions_col2:
        if st.button("🎯 Update Goals"):
            st.session_state.show_goals = True
    with quick_actions_col3:
        if st.button("📚 Browse Resources"):
            st.session_state.page = "Resources"

    # Progress Overview
    st.markdown("---")
    st.subheader("Your Learning Journey 🚀")
    
    # Skill Development Progress with detailed breakdown
    progress_col1, progress_col2 = st.columns([2, 1])
    
    with progress_col1:
        st.markdown("### Skill Development")
        
        # Technical Skills
        tech_skills = {
            "Programming": 75,
            "Data Analysis": 60,
            "Web Development": 45,
            "Problem Solving": 80
        }
        
        for skill, value in tech_skills.items():
            col1, col2, col3 = st.columns([3, 6, 1])
            with col1:
                st.write(f"**{skill}**")
            with col2:
                st.progress(value/100)
            with col3:
                st.write(f"{value}%")
        
        # Soft Skills
        st.markdown("### Soft Skills")
        soft_skills = {
            "Communication": 85,
            "Leadership": 70,
            "Teamwork": 90,
            "Time Management": 65
        }
        
        for skill, value in soft_skills.items():
            col1, col2, col3 = st.columns([3, 6, 1])
            with col1:
                st.write(f"**{skill}**")
            with col2:
                st.progress(value/100)
            with col3:
                st.write(f"{value}%")
    
    with progress_col2:
        # Overall Progress Chart
        st.markdown("### Overall Progress")
        progress_data = pd.DataFrame({
            'Category': ['Technical', 'Soft Skills', 'Projects', 'Certifications'],
            'Progress': [65, 78, 45, 30]
        })
        
        fig = px.pie(progress_data, values='Progress', names='Category',
                    title='Progress Distribution',
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)

    # Goals and Milestones
    st.markdown("---")
    st.subheader("Goals & Milestones 🎯")
    
    # Timeline of goals
    timeline_col1, timeline_col2 = st.columns([3, 1])
    
    with timeline_col1:
        goals = {
            "Short-term Goals": [
                {"goal": "Complete Python Certification", "deadline": "2 weeks", "progress": 60},
                {"goal": "Finish Portfolio Project", "deadline": "1 month", "progress": 30}
            ],
            "Long-term Goals": [
                {"goal": "Master Data Science", "deadline": "6 months", "progress": 25},
                {"goal": "Land Dream Job", "deadline": "1 year", "progress": 15}
            ]
        }
        
        for goal_type, goal_list in goals.items():
            st.markdown(f"### {goal_type}")
            for goal in goal_list:
                col1, col2, col3, col4 = st.columns([3, 2, 4, 1])
                with col1:
                    st.write(f"**{goal['goal']}**")
                with col2:
                    st.write(f"Due: {goal['deadline']}")
                with col3:
                    st.progress(goal['progress']/100)
                with col4:
                    st.write(f"{goal['progress']}%")
    
    with timeline_col2:
        if st.button("➕ Add New Goal"):
            st.session_state.show_add_goal = True

    # Achievements Section
    st.markdown("---")
    st.subheader("Recent Achievements 🏆")
    
    achievements_col1, achievements_col2, achievements_col3 = st.columns(3)
    
    with achievements_col1:
        st.markdown("""
        🌟 **Skills Mastered**
        - Python Programming
        - Data Analysis
        - Project Management
        """)
    
    with achievements_col2:
        st.markdown("""
        📜 **Certifications**
        - Web Development Basics
        - Agile Methodology
        - Leadership 101
        """)
    
    with achievements_col3:
        st.markdown("""
        🎯 **Completed Goals**
        - Created Portfolio
        - Completed 5 Projects
        - Joined Tech Community
        """)

    # Activity Calendar
    st.markdown("---")
    st.subheader("Activity Calendar 📅")
    
    # Sample activity data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    activities = np.random.randint(0, 5, size=len(dates))
    activity_data = pd.DataFrame({
        'date': dates,
        'activity': activities
    })
    
    fig = px.scatter(activity_data, x='date', y='activity',
                    title='Your Learning Activity',
                    labels={'date': 'Date', 'activity': 'Activity Level'},
                    color='activity',
                    size='activity')
    st.plotly_chart(fig)

    # Recommendations
    st.markdown("---")
    st.subheader("Personalized Recommendations 💡")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
        ### Suggested Next Steps
        1. Complete Python Advanced Course
        2. Start Machine Learning Project
        3. Join Tech Community Events
        """)
    
    with rec_col2:
        st.markdown("""
        ### Trending in Your Field
        1. AI/ML Development
        2. Cloud Computing
        3. Data Engineering
        """)