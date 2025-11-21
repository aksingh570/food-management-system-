"""
Smart Food Donation and Waste Management System
Enhanced Production-Ready Version with Modern UI/UX
"""

import streamlit as st
import sqlite3
import hashlib
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import base64
import time
import json

# Page Configuration
st.set_page_config(
    page_title="Smart Food Donation System",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Enhanced Custom CSS with Dark/Light Mode
def get_custom_css(theme='light'):
    if theme == 'dark':
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            
            * {
                font-family: 'Poppins', sans-serif;
            }
            
            .main {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            }
            
            .main-header {
                font-size: 3.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: 700;
                animation: fadeInDown 1s;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 25px;
                border-radius: 15px;
                color: white;
                text-align: center;
                box-shadow: 0 8px 16px rgba(102,126,234,0.3);
                transition: all 0.3s ease;
                animation: fadeInUp 0.8s;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(102,126,234,0.4);
            }
            
            .donation-card {
                border: none;
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                border: 1px solid rgba(255,255,255,0.1);
            }
            
            .donation-card:hover {
                transform: scale(1.02);
                box-shadow: 0 8px 16px rgba(102,126,234,0.3);
            }
            
            .badge {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 5px;
                animation: pulse 2s infinite;
            }
            
            .badge-gold {
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                color: #000;
            }
            
            .badge-silver {
                background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
                color: #000;
            }
            
            .badge-bronze {
                background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);
                color: #fff;
            }
            
            .hero-section {
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
                border-radius: 20px;
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
                animation: fadeIn 1s;
            }
            
            .metric-container {
                background: rgba(255,255,255,0.05);
                padding: 15px;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .stButton>button {
                width: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-weight: 600;
                border: none;
                padding: 14px;
                border-radius: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(102,126,234,0.3);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(102,126,234,0.5);
            }
            
            .success-story {
                background: linear-gradient(135deg, rgba(76,175,80,0.2) 0%, rgba(46,125,50,0.2) 100%);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0;
                border-left: 4px solid #4CAF50;
                backdrop-filter: blur(10px);
            }
            
            .leaderboard-item {
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                display: flex;
                align-items: center;
                justify-content: space-between;
                transition: all 0.3s ease;
                border: 1px solid rgba(255,255,255,0.1);
            }
            
            .leaderboard-item:hover {
                transform: translateX(5px);
                background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
            }
            
            .stProgress > div > div {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }
        </style>
        """
    else:
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            
            * {
                font-family: 'Poppins', sans-serif;
            }
            
            .main {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            
            .main-header {
                font-size: 3.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: 700;
                animation: fadeInDown 1s;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 25px;
                border-radius: 15px;
                color: white;
                text-align: center;
                box-shadow: 0 8px 16px rgba(102,126,234,0.3);
                transition: all 0.3s ease;
                animation: fadeInUp 0.8s;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(102,126,234,0.4);
            }
            
            .donation-card {
                border: none;
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
                background: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .donation-card:hover {
                transform: scale(1.02);
                box-shadow: 0 8px 16px rgba(102,126,234,0.2);
            }
            
            .badge {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 5px;
                animation: pulse 2s infinite;
            }
            
            .badge-gold {
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                color: #000;
            }
            
            .badge-silver {
                background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
                color: #000;
            }
            
            .badge-bronze {
                background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);
                color: #fff;
            }
            
            .hero-section {
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
                border-radius: 20px;
                margin-bottom: 30px;
                animation: fadeIn 1s;
            }
            
            .metric-container {
                background: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .stButton>button {
                width: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-weight: 600;
                border: none;
                padding: 14px;
                border-radius: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(102,126,234,0.3);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(102,126,234,0.5);
            }
            
            .success-story {
                background: linear-gradient(135deg, #4CAF5022 0%, #2E7D3222 100%);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0;
                border-left: 4px solid #4CAF50;
            }
            
            .leaderboard-item {
                background: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .leaderboard-item:hover {
                transform: translateX(5px);
                box-shadow: 0 4px 8px rgba(102,126,234,0.2);
            }
            
            .stProgress > div > div {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }
        </style>
        """

st.markdown(get_custom_css(st.session_state.theme), unsafe_allow_html=True)

# Database Setup with enhanced schema
@st.cache_resource
def init_database():
    conn = sqlite3.connect('food_donation.db', check_same_thread=False)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT,
        role TEXT CHECK(role IN ('donor', 'ngo', 'admin')),
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        verified INTEGER DEFAULT 0,
        profile_pic TEXT,
        total_donations INTEGER DEFAULT 0,
        streak_days INTEGER DEFAULT 0,
        last_donation_date DATE
    )''')
    
    # NGO Profiles
    c.execute('''CREATE TABLE IF NOT EXISTS ngo_profiles (
        ngo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        organization_name TEXT NOT NULL,
        registration_number TEXT UNIQUE,
        address TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        verified INTEGER DEFAULT 0,
        capacity INTEGER DEFAULT 50,
        total_pickups INTEGER DEFAULT 0,
        rating REAL DEFAULT 5.0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')
    
    # Donations table with image support
    c.execute('''CREATE TABLE IF NOT EXISTS donations (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        food_name TEXT NOT NULL,
        quantity TEXT NOT NULL,
        food_type TEXT,
        expiry_time TIMESTAMP NOT NULL,
        location TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        image_data TEXT,
        description TEXT,
        status TEXT DEFAULT 'pending',
        qr_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        collected_at TIMESTAMP,
        view_count INTEGER DEFAULT 0,
        FOREIGN KEY (donor_id) REFERENCES users(user_id)
    )''')
    
    # Requests table
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donation_id INTEGER NOT NULL,
        ngo_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        message TEXT,
        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        accepted_at TIMESTAMP,
        collected_at TIMESTAMP,
        feedback TEXT,
        rating INTEGER,
        FOREIGN KEY (donation_id) REFERENCES donations(donation_id),
        FOREIGN KEY (ngo_id) REFERENCES ngo_profiles(ngo_id)
    )''')
    
    # Success Stories
    c.execute('''CREATE TABLE IF NOT EXISTS success_stories (
        story_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donation_id INTEGER,
        ngo_id INTEGER,
        title TEXT NOT NULL,
        story TEXT NOT NULL,
        impact_meals INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        featured INTEGER DEFAULT 0,
        FOREIGN KEY (donation_id) REFERENCES donations(donation_id),
        FOREIGN KEY (ngo_id) REFERENCES ngo_profiles(ngo_id)
    )''')
    
    # Create admin user
    admin_email = "admin@fooddonation.com"
    admin_pass = hash_password("admin123")
    try:
        c.execute('''INSERT OR IGNORE INTO users (email, password_hash, full_name, role, verified)
                     VALUES (?, ?, ?, ?, ?)''', 
                  (admin_email, admin_pass, "System Admin", "admin", 1))
    except:
        pass
    
    conn.commit()
    return conn

# Utility Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    return hash_password(password) == password_hash

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def image_to_base64(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return base64.b64encode(bytes_data).decode()
    return None

def get_user_badges(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT total_donations, streak_days FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    
    badges = []
    if result:
        total, streak = result[0] or 0, result[1] or 0
        
        if total >= 50:
            badges.append(("🏆", "Gold Donor", "badge-gold"))
        elif total >= 20:
            badges.append(("🥈", "Silver Donor", "badge-silver"))
        elif total >= 5:
            badges.append(("🥉", "Bronze Donor", "badge-bronze"))
        
        if streak >= 7:
            badges.append(("🔥", f"{streak} Day Streak", "badge-gold"))
        
    return badges

# Authentication Functions
def register_user(conn, email, password, full_name, phone, role):
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        c.execute('''INSERT INTO users (email, password_hash, full_name, phone, role)
                     VALUES (?, ?, ?, ?, ?)''',
                  (email, password_hash, full_name, phone, role))
        conn.commit()
        return True, c.lastrowid
    except sqlite3.IntegrityError:
        return False, "Email already exists"

def login_user(conn, email, password):
    c = conn.cursor()
    c.execute("SELECT user_id, password_hash, full_name, role, verified FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    
    if result and verify_password(password, result[1]):
        return True, {
            'user_id': result[0],
            'name': result[2],
            'role': result[3],
            'verified': result[4],
            'email': email
        }
    return False, None

# Enhanced Home Page
def show_home_page(conn):
    st.markdown('<h1 class="main-header">🍱 Smart Food Donation System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class='hero-section'>
        <h2 style='color: #667eea; margin-bottom: 10px;'>Connecting Surplus Food with Those Who Need It Most</h2>
        <p style='font-size: 1.2rem; color: #555;'>Every year, millions of tons of food are wasted while many go hungry. 
        Our platform bridges this gap by connecting food donors with NGOs and volunteers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time Statistics with animations
    col1, col2, col3, col4 = st.columns(4)
    
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM donations WHERE status='completed'")
    total_donations = c.fetchone()[0]
    
    c.execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE role='ngo' AND verified=1")
    total_ngos = c.fetchone()[0]
    
    c.execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE role='donor'")
    total_donors = c.fetchone()[0]
    
    meals_saved = total_donations * 15
    food_saved_kg = total_donations * 5
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <h2 style='font-size: 2.5rem; margin: 0;'>{total_donations}</h2>
            <p style='margin: 5px 0; opacity: 0.9;'>Donations Completed</p>
            <p style='font-size: 0.9rem; opacity: 0.7;'>🎯 Making Impact</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <h2 style='font-size: 2.5rem; margin: 0;'>{total_ngos}</h2>
            <p style='margin: 5px 0; opacity: 0.9;'>NGOs Partnered</p>
            <p style='font-size: 0.9rem; opacity: 0.7;'>❤️ Verified Partners</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card'>
            <h2 style='font-size: 2.5rem; margin: 0;'>{meals_saved:,}</h2>
            <p style='margin: 5px 0; opacity: 0.9;'>Meals Served</p>
            <p style='font-size: 0.9rem; opacity: 0.7;'>🍽️ Lives Touched</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <h2 style='font-size: 2.5rem; margin: 0;'>{food_saved_kg:,} kg</h2>
            <p style='margin: 5px 0; opacity: 0.9;'>Food Saved</p>
            <p style='font-size: 0.9rem; opacity: 0.7;'>🌍 Waste Reduced</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Success Stories
    st.markdown("### 🌟 Recent Success Stories")
    
    c.execute('''SELECT s.title, s.story, s.impact_meals, s.created_at, n.organization_name
                 FROM success_stories s
                 JOIN ngo_profiles n ON s.ngo_id = n.ngo_id
                 ORDER BY s.created_at DESC LIMIT 3''')
    stories = c.fetchall()
    
    if stories:
        for story in stories:
            st.markdown(f"""
            <div class='success-story'>
                <h4>✨ {story[0]}</h4>
                <p style='margin: 10px 0;'>{story[1]}</p>
                <p style='font-size: 0.9rem; color: #4CAF50;'>
                    <strong>{story[4]}</strong> • {story[2]} meals served • {story[3][:10]}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🎯 Be part of our first success story! Start donating today.")
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("### 🎯 Join Our Mission Today")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎁 Donate Food Now", key="home_donate", use_container_width=True):
                st.session_state.page = "register"
                st.session_state.register_role = "donor"
                st.rerun()
        with col_b:
            if st.button("❤️ Join as NGO", key="home_ngo", use_container_width=True):
                st.session_state.page = "register"
                st.session_state.register_role = "ngo"
                st.rerun()
    
    # How it works with enhanced styling
    st.markdown("---")
    st.markdown("### 📖 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); border-radius: 15px; border: 2px solid #667eea33;'>
            <div style='font-size: 3rem; margin-bottom: 10px;'>1️⃣</div>
            <h3 style='color: #667eea; margin: 10px 0;'>Post Donation</h3>
            <p style='color: #666;'>Restaurants, events, or individuals post surplus food details with photos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); border-radius: 15px; border: 2px solid #667eea33;'>
            <div style='font-size: 3rem; margin-bottom: 10px;'>2️⃣</div>
            <h3 style='color: #667eea; margin: 10px 0;'>NGOs Request</h3>
            <p style='color: #666;'>Nearby NGOs get instant notifications and request pickup with one click</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); border-radius: 15px; border: 2px solid #667eea33;'>
            <div style='font-size: 3rem; margin-bottom: 10px;'>3️⃣</div>
            <h3 style='color: #667eea; margin: 10px 0;'>Food Delivered</h3>
            <p style='color: #666;'>Food is collected using QR codes and distributed to those in need</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live Donation Feed
    st.markdown("---")
    st.markdown("### 🔴 Live Donation Feed")
    
    c.execute('''SELECT d.food_name, d.quantity, d.location, d.created_at, u.full_name
                 FROM donations d
                 JOIN users u ON d.donor_id = u.user_id
                 WHERE d.status = 'pending'
                 ORDER BY d.created_at DESC LIMIT 5''')
    live_donations = c.fetchall()
    
    if live_donations:
        for don in live_donations:
            time_ago = (datetime.now() - datetime.strptime(don[3], '%Y-%m-%d %H:%M:%S')).seconds // 60
            st.markdown(f"""
            <div class='donation-card' style='padding: 15px;'>
                <strong>🍱 {don[0]}</strong> ({don[1]}) • 📍 {don[2]} • 
                <span style='color: #4CAF50;'>Posted {time_ago}min ago by {don[4]}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 No active donations right now. Be the first to donate!")

# Enhanced Donor Dashboard
def show_donor_dashboard(conn, user_id):
    st.title("🎁 Donor Dashboard")
    
    # User badges and stats
    badges = get_user_badges(conn, user_id)
    if badges:
        badge_html = "".join([f"<span class='badge {badge[2]}'>{badge[0]} {badge[1]}</span>" for badge in badges])
        st.markdown(f"""
        <div style='text-align: center; margin: 20px 0;'>
            <h3>Your Achievements</h3>
            {badge_html}
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Post Donation", "📋 My Donations", "📊 My Impact", "🌟 Success Stories"])
    
    with tab1:
        st.subheader("Create New Food Donation")
        
        with st.form("donation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                food_name = st.text_input("🍱 Food Item Name *", placeholder="e.g., Biryani, Pizza, Rice")
                quantity = st.text_input("📦 Quantity *", placeholder="e.g., 50 plates, 10 kg")
                food_type = st.selectbox("🍽️ Food Type *", 
                    ["Cooked Food", "Raw Food", "Packaged Food", "Fruits/Vegetables", "Bakery Items"])
            
            with col2:
                expiry_date = st.date_input("📅 Expiry Date", 
                    min_value=datetime.now().date(),
                    value=datetime.now().date())
                expiry_time = st.time_input("⏰ Expiry Time", value=datetime.now().time())
                location = st.text_input("📍 Pickup Location *", placeholder="e.g., Green Valley Restaurant, Sector 18")
            
            # Image upload
            uploaded_image = st.file_uploader("📸 Upload Food Image (Optional)", type=['jpg', 'jpeg', 'png'])
            if uploaded_image:
                st.image(uploaded_image, caption="Preview", width=300)
            
            description = st.text_area("📝 Additional Details", placeholder="Any special instructions or details...")
            
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("🌐 Latitude", value=28.5355, format="%.6f", 
                    help="You can get this from Google Maps")
            with col2:
                longitude = st.number_input("🌐 Longitude", value=77.3910, format="%.6f",
                    help="You can get this from Google Maps")
            
            submit = st.form_submit_button("🚀 Post Donation", use_container_width=True)
            
            if submit:
                if food_name and quantity and location:
                    expiry_datetime = datetime.combine(expiry_date, expiry_time)
                    
                    c = conn.cursor()
                    qr_data = f"DONATION-{datetime.now().strftime('%Y%m%d%H%M%S')}-{user_id}"
                    qr_code = generate_qr_code(qr_data)
                    
                    image_data = image_to_base64(uploaded_image) if uploaded_image else None
                    
                    c.execute('''INSERT INTO donations 
                                (donor_id, food_name, quantity, food_type, expiry_time, location, latitude, longitude, description, qr_code, image_data)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, food_name, quantity, food_type, expiry_datetime, location, latitude, longitude, description, qr_code, image_data))
                    
                    # Update user stats
                    c.execute("UPDATE users SET total_donations = total_donations + 1, last_donation_date = ? WHERE user_id = ?",
                             (datetime.now().date(), user_id))
                    
                    conn.commit()
                    
                    st.success("✅ Donation posted successfully! NGOs will be notified.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("⚠️ Please fill all required fields (*)")
    
    with tab2:
        st.subheader("Your Posted Donations")
        
        # Filter options
        status_filter = st.selectbox("Filter by Status", ["All", "pending", "accepted", "completed"])
        
        c = conn.cursor()
        if status_filter == "All":
            c.execute('''SELECT donation_id, food_name, quantity, location, status, created_at, qr_code, expiry_time, image_data
                         FROM donations WHERE donor_id = ? ORDER BY created_at DESC''', (user_id,))
        else:
            c.execute('''SELECT donation_id, food_name, quantity, location, status, created_at, qr_code, expiry_time, image_data
                         FROM donations WHERE donor_id = ? AND status = ? ORDER BY created_at DESC''', (user_id, status_filter))
        donations = c.fetchall()
        
        if donations:
            for don in donations:
                status_emoji = {"pending": "⏳", "accepted": "✅", "completed": "🎉", "expired": "❌"}
                with st.expander(f"{status_emoji.get(don[4], '📋')} {don[1]} - {don[2]} ({don[4].upper()})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        if don[8]:  # If image exists
                            st.image(f"data:image/png;base64,{don[8]}", width=300)
                        
                        st.write(f"**📍 Location:** {don[3]}")
                        st.write(f"**📅 Posted:** {don[5]}")
                        st.write(f"**⏰ Expires:** {don[7]}")
                        st.write(f"**📊 Status:** {don[4].upper()}")
                        
                        # Show requests
                        c.execute('''SELECT r.request_id, r.status, n.organization_name, u.phone, u.email
                                    FROM requests r
                                    JOIN ngo_profiles n ON r.ngo_id = n.ngo_id
                                    JOIN users u ON n.user_id = u.user_id
                                    WHERE r.donation_id = ?''', (don[0],))
                        requests = c.fetchall()
                        
                        if requests:
                            st.write("**📞 Pickup Requests:**")
                            for req in requests:
                                st.markdown(f"""
                                <div class='donation-card' style='padding: 10px; margin: 5px 0;'>
                                    <strong>{req[2]}</strong> ({req[1]}) <br>
                                    📧 {req[4]} | 📱 {req[3] or 'N/A'}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if req[1] == 'pending' and don[4] == 'pending':
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        if st.button(f"✅ Accept", key=f"accept_{req[0]}"):
                                            c.execute("UPDATE requests SET status='accepted', accepted_at=? WHERE request_id=?",
                                                     (datetime.now(), req[0]))
                                            c.execute("UPDATE donations SET status='accepted' WHERE donation_id=?", (don[0],))
                                            conn.commit()
                                            st.success("Request accepted!")
                                            st.rerun()
                                    with col_b:
                                        if st.button(f"❌ Reject", key=f"reject_{req[0]}"):
                                            c.execute("DELETE FROM requests WHERE request_id=?", (req[0],))
                                            conn.commit()
                                            st.info("Request rejected")
                                            st.rerun()
                        else:
                            st.info("No pickup requests yet")
                    
                    with col2:
                        if don[6]:
                            st.image(f"data:image/png;base64,{don[6]}", caption="QR Code", width=150)
                            st.download_button("📥 Download QR", 
                                data=base64.b64decode(don[6]),
                                file_name=f"donation_{don[0]}.png",
                                mime="image/png",
                                key=f"qr_{don[0]}")
        else:
            st.info("📭 No donations found. Create your first donation!")
    
    with tab3:
        st.subheader("Your Impact Dashboard")
        
        c = conn.cursor()
        c.execute('''SELECT COUNT(*), 
                            SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END),
                            SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END),
                            SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END)
                     FROM donations WHERE donor_id = ?''', (user_id,))
        total, completed, pending, accepted = c.fetchone()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #667eea; margin: 0;'>{total or 0}</h2>
                <p style='margin: 5px 0;'>📊 Total Donations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #4CAF50; margin: 0;'>{completed or 0}</h2>
                <p style='margin: 5px 0;'>✅ Completed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #FFA500; margin: 0;'>{pending or 0}</h2>
                <p style='margin: 5px 0;'>⏳ Pending</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #2196F3; margin: 0;'>{accepted or 0}</h2>
                <p style='margin: 5px 0;'>🤝 Accepted</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            meals = (completed or 0) * 15
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #667eea;'>🍽️ {meals:,}</h2>
                <p>Estimated Meals Served</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            food_saved = (completed or 0) * 5
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #4CAF50;'>⚖️ {food_saved} kg</h2>
                <p>Estimated Food Saved</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        st.markdown("---")
        st.subheader("📈 Your Activity Over Time")
        
        c.execute('''SELECT DATE(created_at) as date, COUNT(*) as count
                     FROM donations WHERE donor_id = ?
                     GROUP BY DATE(created_at)
                     ORDER BY date DESC LIMIT 30''', (user_id,))
        chart_data = c.fetchall()
        
        if chart_data:
            df = pd.DataFrame(chart_data, columns=['Date', 'Donations'])
            fig = px.line(df, x='Date', y='Donations', title='Your Donation Activity',
                         markers=True, line_shape='spline')
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        # Donation type distribution
        c.execute('''SELECT food_type, COUNT(*) as count
                     FROM donations WHERE donor_id = ?
                     GROUP BY food_type''', (user_id,))
        type_data = c.fetchall()
        
        if type_data:
            df_type = pd.DataFrame(type_data, columns=['Type', 'Count'])
            fig2 = px.pie(df_type, values='Count', names='Type', title='Donations by Food Type',
                         hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab4:
        st.subheader("🌟 Share Your Success Story")
        
        with st.form("success_story_form"):
            story_title = st.text_input("Story Title", placeholder="A memorable donation experience")
            story_text = st.text_area("Your Story", placeholder="Tell us about the impact of your donation...")
            
            c = conn.cursor()
            c.execute('''SELECT d.donation_id, d.food_name, d.created_at
                         FROM donations d
                         WHERE d.donor_id = ? AND d.status = 'completed'
                         ORDER BY d.created_at DESC LIMIT 10''', (user_id,))
            completed_donations = c.fetchall()
            
            if completed_donations:
                donation_options = [f"{d[1]} - {d[2][:10]}" for d in completed_donations]
                selected_donation = st.selectbox("Related Donation", donation_options)
            
            submit_story = st.form_submit_button("✨ Share Story", use_container_width=True)
            
            if submit_story and story_title and story_text:
                st.success("✅ Story submitted for review! Thank you for sharing.")
                st.balloons()

# Enhanced NGO Dashboard
def show_ngo_dashboard(conn, user_id):
    st.title("❤️ NGO Dashboard")
    
    c = conn.cursor()
    c.execute("SELECT ngo_id, organization_name, verified, total_pickups FROM ngo_profiles WHERE user_id = ?", (user_id,))
    ngo_profile = c.fetchone()
    
    if not ngo_profile:
        st.warning("⚠️ Please complete your NGO profile first.")
        
        with st.form("ngo_profile_form"):
            st.subheader("Complete Your NGO Profile")
            
            org_name = st.text_input("Organization Name *")
            reg_number = st.text_input("Registration Number *")
            address = st.text_area("Complete Address *")
            
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=28.5355, format="%.6f")
            with col2:
                longitude = st.number_input("Longitude", value=77.3910, format="%.6f")
            
            capacity = st.number_input("Daily Capacity (meals)", min_value=10, value=50)
            
            submit = st.form_submit_button("✨ Submit Profile", use_container_width=True)
            
            if submit:
                if org_name and reg_number and address:
                    c.execute('''INSERT INTO ngo_profiles 
                                (user_id, organization_name, registration_number, address, latitude, longitude, capacity)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, org_name, reg_number, address, latitude, longitude, capacity))
                    conn.commit()
                    st.success("✅ Profile created! Waiting for admin verification.")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill all required fields")
        return
    
    ngo_id, org_name, verified, total_pickups = ngo_profile
    
    if not verified:
        st.warning("⏳ Your NGO profile is pending admin verification. You'll be notified once approved.")
        return
    
    st.success(f"✅ Welcome, {org_name}!")
    
    # NGO Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Total Pickups", total_pickups or 0)
    with col2:
        st.metric("🍽️ People Fed", (total_pickups or 0) * 15)
    with col3:
        c.execute("SELECT AVG(rating) FROM requests WHERE ngo_id = ? AND rating IS NOT NULL", (ngo_id,))
        avg_rating = c.fetchone()[0] or 5.0
        st.metric("⭐ Rating", f"{avg_rating:.1f}/5.0")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Browse Donations", "📦 My Requests", "📊 Impact", "🗺️ Map View"])
    
    with tab1:
        st.subheader("Available Food Donations")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            food_filter = st.selectbox("Filter by Type", ["All", "Cooked Food", "Raw Food", "Packaged Food", "Fruits/Vegetables", "Bakery Items"])
        with col2:
            distance_filter = st.slider("Max Distance (km)", 1, 50, 20)
        with col3:
            search_term = st.text_input("🔍 Search", placeholder="Search food items...")
        
        c.execute("SELECT latitude, longitude FROM ngo_profiles WHERE ngo_id = ?", (ngo_id,))
        ngo_lat, ngo_lon = c.fetchone()
        
        query = '''SELECT d.donation_id, d.food_name, d.quantity, d.food_type, d.location, 
                          d.expiry_time, d.latitude, d.longitude, d.description, u.full_name, u.phone, u.email, d.image_data
                   FROM donations d
                   JOIN users u ON d.donor_id = u.user_id
                   WHERE d.status = 'pending' '''
        
        if food_filter != "All":
            query += f" AND d.food_type = '{food_filter}'"
        
        if search_term:
            query += f" AND (d.food_name LIKE '%{search_term}%' OR d.description LIKE '%{search_term}%')"
        
        query += " ORDER BY d.created_at DESC"
        
        c.execute(query)
        donations = c.fetchall()
        
        if donations:
            for don in donations:
                distance = ((don[6] - ngo_lat)**2 + (don[7] - ngo_lon)**2)**0.5 * 111
                
                if distance <= distance_filter:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class='donation-card'>
                                <h4>🍱 {don[1]} ({don[2]})</h4>
                                <p><strong>Type:</strong> {don[3]} | <strong>Location:</strong> {don[4]}</p>
                                <p><strong>Expires:</strong> {don[5]} | <strong>Distance:</strong> ~{distance:.1f} km</p>
                                <p><strong>Details:</strong> {don[8] or 'No additional details'}</p>
                                <p><strong>Contact:</strong> {don[9]} | 📧 {don[11]} | 📱 {don[10] or 'N/A'}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if don[12]:  # If image exists
                                st.image(f"data:image/png;base64,{don[12]}", width=150)
                        
                        c.execute("SELECT status FROM requests WHERE donation_id = ? AND ngo_id = ?", 
                                 (don[0], ngo_id))
                        existing_request = c.fetchone()
                        
                        if existing_request:
                            st.info(f"📋 Status: {existing_request[0].upper()}")
                        else:
                            if st.button(f"🚀 Request Pickup", key=f"req_{don[0]}", use_container_width=True):
                                c.execute('''INSERT INTO requests (donation_id, ngo_id, message)
                                            VALUES (?, ?, ?)''',
                                         (don[0], ngo_id, f"Pickup request from {org_name}"))
                                conn.commit()
                                st.success("✅ Request sent to donor!")
                                st.balloons()
                                st.rerun()
                        
                        st.markdown("---")
        else:
            st.info("📭 No donations available matching your criteria.")
    
    with tab2:
        st.subheader("Your Pickup Requests")
        
        status_filter_req = st.selectbox("Filter Status", ["All", "pending", "accepted", "completed"])
        
        if status_filter_req == "All":
            c.execute('''SELECT r.request_id, r.status, d.food_name, d.quantity, d.location, 
                                d.latitude, d.longitude, u.full_name, u.phone, u.email, r.requested_at, d.donation_id, d.image_data
                         FROM requests r
                         JOIN donations d ON r.donation_id = d.donation_id
                         JOIN users u ON d.donor_id = u.user_id
                         WHERE r.ngo_id = ?
                         ORDER BY r.requested_at DESC''', (ngo_id,))
        else:
            c.execute('''SELECT r.request_id, r.status, d.food_name, d.quantity, d.location, 
                                d.latitude, d.longitude, u.full_name, u.phone, u.email, r.requested_at, d.donation_id, d.image_data
                         FROM requests r
                         JOIN donations d ON r.donation_id = d.donation_id
                         JOIN users u ON d.donor_id = u.user_id
                         WHERE r.ngo_id = ? AND r.status = ?
                         ORDER BY r.requested_at DESC''', (ngo_id, status_filter_req))
        
        requests = c.fetchall()
        
        if requests:
            for req in requests:
                status_emoji = {"pending": "⏳", "accepted": "✅", "completed": "🎉"}
                with st.expander(f"{status_emoji.get(req[1], '📋')} {req[2]} - {req[1].upper()}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**🍱 Food:** {req[2]} ({req[3]})")
                        st.write(f"**📍 Location:** {req[4]}")
                        st.write(f"**👤 Donor:** {req[7]}")
                        st.write(f"**📧 Email:** {req[9]}")
                        st.write(f"**📱 Phone:** {req[8] or 'N/A'}")
                        st.write(f"**📅 Requested:** {req[10]}")
                        
                        if req[1] == "accepted":
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("✅ Mark as Collected", key=f"collect_{req[0]}"):
                                    c.execute("UPDATE requests SET status='completed', collected_at=? WHERE request_id=?",
                                             (datetime.now(), req[0]))
                                    c.execute("UPDATE donations SET status='completed' WHERE donation_id = ?",
                                             (req[11],))
                                    c.execute("UPDATE ngo_profiles SET total_pickups = total_pickups + 1 WHERE ngo_id = ?",
                                             (ngo_id,))
                                    conn.commit()
                                    st.success("✅ Marked as collected!")
                                    st.balloons()
                                    st.rerun()
                            
                            with col_b:
                                map_url = f"https://www.google.com/maps/dir/?api=1&destination={req[5]},{req[6]}"
                                st.link_button("🗺️ Get Directions", map_url)
                    
                    with col2:
                        if req[12]:
                            st.image(f"data:image/png;base64,{req[12]}", width=200)
        else:
            st.info("📭 No pickup requests found.")
    
    with tab3:
        st.subheader("Your Impact Summary")
        
        c.execute('''SELECT COUNT(*), 
                            SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END),
                            SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END),
                            SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END)
                     FROM requests WHERE ngo_id = ?''', (ngo_id,))
        total_req, completed, pending, accepted = c.fetchone()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #667eea;'>{total_req or 0}</h2>
                <p>📊 Total Requests</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #4CAF50;'>{completed or 0}</h2>
                <p>✅ Completed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #FFA500;'>{pending or 0}</h2>
                <p>⏳ Pending</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #2196F3;'>{accepted or 0}</h2>
                <p>🤝 Accepted</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #667eea;'>🍽️ {(completed or 0) * 15:,}</h2>
                <p>People Fed (Estimated)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-container'>
                <h2 style='color: #4CAF50;'>⚖️ {(completed or 0) * 5} kg</h2>
                <p>Food Collected</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Activity chart
        st.markdown("---")
        st.subheader("📈 Your Pickup Activity")
        
        c.execute('''SELECT DATE(requested_at) as date, COUNT(*) as count
                     FROM requests WHERE ngo_id = ?
                     GROUP BY DATE(requested_at)
                     ORDER BY date DESC LIMIT 30''', (ngo_id,))
        activity_data = c.fetchall()
        
        if activity_data:
            df = pd.DataFrame(activity_data, columns=['Date', 'Requests'])
            fig = px.bar(df, x='Date', y='Requests', title='Request Activity Over Time')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🗺️ Nearby Donations Map")
        st.info("📍 This feature shows nearby food donations on an interactive map")
        
        c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.latitude, d.longitude, d.location
                     FROM donations d
                     WHERE d.status = 'pending'
                     ORDER BY d.created_at DESC LIMIT 20''')
        map_donations = c.fetchall()
        
        if map_donations:
            map_data = pd.DataFrame(map_donations, columns=['ID', 'Food', 'Quantity', 'lat', 'lon', 'Location'])
            st.map(map_data[['lat', 'lon']])
            
            st.dataframe(map_data[['Food', 'Quantity', 'Location']], use_container_width=True, hide_index=True)
        else:
            st.info("No active donations to display on map")

# Enhanced Admin Panel  
def show_admin_panel(conn):
    st.title("🔧 Admin Dashboard")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "✅ Verify NGOs", "👥 Users", "📈 Analytics", "🏆 Leaderboard"])
    
    with tab1:
        st.subheader("System Overview")
        
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM users WHERE role='donor'")
        total_donors = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE role='ngo'")
        total_ngos = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM donations")
        total_donations = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM donations WHERE status='completed'")
        completed_donations = c.fetchone()[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='stat-card'>
                <h2>{total_donors}</h2>
                <p>👥 Total Donors</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='stat-card'>
                <h2>{total_ngos}</h2>
                <p>🏢 Total NGOs</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='stat-card'>
                <h2>{total_donations}</h2>
                <p>📦 Total Donations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='stat-card'>
                <h2>{completed_donations}</h2>
                <p>✅ Completed</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📋 Recent Donations")
        
        c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.status, d.created_at, u.full_name
                     FROM donations d
                     JOIN users u ON d.donor_id = u.user_id
                     ORDER BY d.created_at DESC LIMIT 15''')
        recent = c.fetchall()
        
        if recent:
            df = pd.DataFrame(recent, columns=['ID', 'Food', 'Quantity', 'Status', 'Date', 'Donor'])
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("NGO Verification Requests")
        
        c.execute('''SELECT n.ngo_id, n.organization_name, n.registration_number, n.address, u.email, u.phone, u.full_name
                     FROM ngo_profiles n
                     JOIN users u ON n.user_id = u.user_id
                     WHERE n.verified = 0''')
        pending_ngos = c.fetchall()
        
        if pending_ngos:
            for ngo in pending_ngos:
                with st.expander(f"📋 {ngo[1]}"):
                    st.write(f"**Contact Person:** {ngo[6]}")
                    st.write(f"**Registration No:** {ngo[2]}")
                    st.write(f"**Address:** {ngo[3]}")
                    st.write(f"**Email:** {ngo[4]}")
                    st.write(f"**Phone:** {ngo[5] or 'N/A'}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Verify & Approve", key=f"verify_{ngo[0]}", use_container_width=True):
                            c.execute("UPDATE ngo_profiles SET verified=1 WHERE ngo_id=?", (ngo[0],))
                            conn.commit()
                            st.success("✅ NGO verified!")
                            st.balloons()
                            st.rerun()
                    with col2:
                        if st.button("❌ Reject", key=f"reject_{ngo[0]}", use_container_width=True):
                            c.execute("DELETE FROM ngo_profiles WHERE ngo_id=?", (ngo[0],))
                            conn.commit()
                            st.warning("NGO rejected")
                            st.rerun()
        else:
            st.success("✅ No pending verification requests.")
    
    with tab3:
        st.subheader("User Management")
        
        filter_role = st.selectbox("Filter by Role", ["All", "donor", "ngo", "admin"])
        
        if filter_role == "All":
            c.execute('''SELECT user_id, email, full_name, role, status, created_at
                         FROM users ORDER BY created_at DESC''')
        else:
            c.execute('''SELECT user_id, email, full_name, role, status, created_at
                         FROM users WHERE role=? ORDER BY created_at DESC''', (filter_role,))
        
        users = c.fetchall()
        
        if users:
            df = pd.DataFrame(users, columns=['ID', 'Email', 'Name', 'Role', 'Status', 'Joined'])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export option
            csv = df.to_csv(index=False)
            st.download_button("📥 Export Users CSV", csv, "users.csv", "text/csv")
    
    with tab4:
        st.subheader("System Analytics")
        
        # Donations over time
        c.execute('''SELECT DATE(created_at) as date, COUNT(*) as count
                     FROM donations
                     GROUP BY DATE(created_at)
                     ORDER BY date DESC LIMIT 30''')
        data = c.fetchall()
        
        if data:
            df = pd.DataFrame(data, columns=['Date', 'Donations'])
            fig = px.line(df, x='Date', y='Donations', title='Donations Over Time', markers=True)
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            c.execute('''SELECT status, COUNT(*) as count
                         FROM donations
                         GROUP BY status''')
            status_data = c.fetchall()
            
            if status_data:
                df_status = pd.DataFrame(status_data, columns=['Status', 'Count'])
                fig2 = px.pie(df_status, values='Count', names='Status', title='Donation Status Distribution', hole=0.4)
                st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Food type distribution
            c.execute('''SELECT food_type, COUNT(*) as count
                         FROM donations
                         GROUP BY food_type
                         ORDER BY count DESC''')
            food_data = c.fetchall()
            
            if food_data:
                df_food = pd.DataFrame(food_data, columns=['Type', 'Count'])
                fig3 = px.bar(df_food, x='Type', y='Count', title='Donations by Food Type')
                st.plotly_chart(fig3, use_container_width=True)
    
    with tab5:
        st.subheader("🏆 Leaderboards")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👑 Top Donors")
            c.execute('''SELECT u.full_name, COUNT(*) as donations
                         FROM donations d
                         JOIN users u ON d.donor_id = u.user_id
                         WHERE d.status = 'completed'
                         GROUP BY d.donor_id
                         ORDER BY donations DESC
                         LIMIT 10''')
            top_donors = c.fetchall()
            
            if top_donors:
                for idx, donor in enumerate(top_donors, 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                    st.markdown(f"""
                    <div class='leaderboard-item'>
                        <span><strong>{medal} {donor[0]}</strong></span>
                        <span><strong>{donor[1]}</strong> donations</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🌟 Top NGOs")
            c.execute('''SELECT n.organization_name, n.total_pickups
                         FROM ngo_profiles n
                         WHERE n.verified = 1
                         ORDER BY n.total_pickups DESC
                         LIMIT 10''')
            top_ngos = c.fetchall()
            
            if top_ngos:
                for idx, ngo in enumerate(top_ngos, 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                    st.markdown(f"""
                    <div class='leaderboard-item'>
                        <span><strong>{medal} {ngo[0]}</strong></span>
                        <span><strong>{ngo[1]}</strong> pickups</span>
                    </div>
                    """, unsafe_allow_html=True)

# Login/Register Page
def show_auth_page(conn):
    default_role = st.session_state.get('register_role', 'donor')
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", key="login_email", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", key="login_password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if email and password:
                    success, user_data = login_user(conn, email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = user_data
                        st.success(f"✅ Welcome back, {user_data['name']}!")
                        st.balloons()
                        st.session_state.page = "dashboard"
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.error("⚠️ Please fill all fields")
        
        st.info("💡 **Demo Credentials:**\n\n• Admin: admin@fooddonation.com / admin123")
    
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("register_form"):
            reg_name = st.text_input("👤 Full Name *", key="reg_name", placeholder="John Doe")
            reg_email = st.text_input("📧 Email *", key="reg_email", placeholder="john@example.com")
            reg_phone = st.text_input("📱 Phone Number", key="reg_phone", placeholder="+91 9876543210")
            reg_password = st.text_input("🔒 Password *", type="password", key="reg_password")
            reg_confirm_password = st.text_input("🔒 Confirm Password *", type="password", key="reg_confirm")
            reg_role = st.selectbox("Register as *", ["donor", "ngo"], index=0 if default_role=="donor" else 1)
            
            submit = st.form_submit_button("✨ Create Account", use_container_width=True)
            
            if submit:
                if not (reg_name and reg_email and reg_password):
                    st.error("⚠️ Please fill all required fields (*)")
                elif reg_password != reg_confirm_password:
                    st.error("⚠️ Passwords don't match")
                elif len(reg_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters")
                else:
                    success, result = register_user(conn, reg_email, reg_password, reg_name, reg_phone, reg_role)
                    if success:
                        st.success("✅ Registration successful! Please login.")
                        st.balloons()
                        
                        if reg_role == "ngo":
                            st.info("📋 As an NGO, please complete your profile after logging in.")
                        
                        time.sleep(1)
                    else:
                        st.error(f"❌ {result}")

# Main Application
def main():
    conn = init_database()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 80px;'>🍱</div>
            <h2 style='color: #667eea; margin: 0;'>Food Donation</h2>
            <p style='color: #666; margin: 0;'>Smart System</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Theme Toggle
        if st.button(f"{'🌙 Dark Mode' if st.session_state.theme == 'light' else '☀️ Light Mode'}", 
                     use_container_width=True):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
        
        st.markdown("---")
        
        if not st.session_state.logged_in:
            st.markdown("### 🚀 Quick Access")
            if st.button("🏠 Home", key="nav_home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
            if st.button("🔐 Login / Register", key="nav_auth", use_container_width=True):
                st.session_state.page = 'auth'
                st.rerun()
        else:
            st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); border-radius: 10px; margin-bottom: 10px;'>
                <p style='margin: 0; color: #4CAF50; font-weight: 600;'>✅ Logged In</p>
                <h4 style='margin: 5px 0; color: #667eea;'>{st.session_state.user['name']}</h4>
                <p style='margin: 0; font-size: 0.9rem; color: #666;'>{st.session_state.user['role'].upper()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            if st.button("🏠 Home", key="nav_home_logged", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
            
            st.markdown("---")
            
            if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.page = 'home'
                st.success("👋 Logged out successfully!")
                time.sleep(0.5)
                st.rerun()
        
        st.markdown("---")
        
        # Quick Stats in Sidebar
        st.markdown("### 📊 Live Stats")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM donations WHERE status='completed'")
        completed = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM donations WHERE status='pending'")
        pending = c.fetchone()[0]
        
        st.markdown(f"""
        <div class='metric-container' style='margin: 10px 0;'>
            <h3 style='color: #4CAF50; margin: 0;'>{completed}</h3>
            <p style='margin: 0; font-size: 0.9rem;'>✅ Completed</p>
        </div>
        <div class='metric-container' style='margin: 10px 0;'>
            <h3 style='color: #FFA500; margin: 0;'>{pending}</h3>
            <p style='margin: 0; font-size: 0.9rem;'>⏳ Active Now</p>
        </div>
        <div class='metric-container' style='margin: 10px 0;'>
            <h3 style='color: #667eea; margin: 0;'>{completed * 15:,}</h3>
            <p style='margin: 0; font-size: 0.9rem;'>🍽️ Meals Saved</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        ### 📞 Contact
        📧 support@fooddonation.com  
        🌐 www.fooddonation.com
        
        ---
        
        <p style='text-align: center; color: #666; font-size: 0.85rem;'>
        💚 Fighting food waste,<br>feeding hope.
        </p>
        """, unsafe_allow_html=True)
    
    # Main content routing
    if st.session_state.page == 'home':
        show_home_page(conn)
    elif st.session_state.page == 'auth' or st.session_state.page == 'register':
        show_auth_page(conn)
    elif st.session_state.page == 'dashboard' and st.session_state.logged_in:
        user_role = st.session_state.user['role']
        user_id = st.session_state.user['user_id']
        
        if user_role == 'donor':
            show_donor_dashboard(conn, user_id)
        elif user_role == 'ngo':
            show_ngo_dashboard(conn, user_id)
        elif user_role == 'admin':
            show_admin_panel(conn)
    else:
        show_home_page(conn)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666;'>
        <p>Made with ❤️ for a better world | © 2024 Smart Food Donation System</p>
        <p style='font-size: 0.85rem;'>Together, we can end food waste and hunger 🌍</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()