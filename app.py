import streamlit as st
import datetime
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Astro Kundali | Premium", page_icon="✨", layout="centered")

# --- CUSTOM CSS (HTML/CSS Design) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #ffffff !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Glassmorphism Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        margin-top: 50px;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #ff4b4b, #ff7676);
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 15px 40px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
        color: white;
    }

    /* Input Fields Styling */
    .stTextInput>div>div>input, .stDateInput>div>div>input, .stTimeInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Success/Info Alerts */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT (Page change karne ke liye) ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# API Key
API_KEY = "13f7f206140dc61917532f1cdbd03421eab2ac967216fe5d50c89b386de12713" # <--- Yahan apni key daalna

# --- PAGE 1: HOME (LANDING PAGE) ---
if st.session_state.page == "home":
    st.markdown("""
        <div class="glass-card">
            <h1>✨ Discover Your Destiny ✨</h1>
            <p style='font-size: 18px; color: #cccccc; margin-bottom: 30px;'>
                Unlock the secrets of the cosmos. Get your accurate birth chart, planetary positions, and Nakshatra analysis based on Vedic Astrology.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Space
    st.write("") 
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("View Your Kundali 🔮"):
            st.session_state.page = "form"
            st.rerun()

# --- PAGE 2: FORM ---
elif st.session_state.page == "form":
    st.markdown("<h1>Enter Your Details</h1>", unsafe_allow_html=True)
    
    with st.form("kundali_form"):
        name = st.text_input("👤 Apna Naam likhein:")
        dob = st.date_input("📅 Date of Birth:", min_value=datetime.date(1950, 1, 1), max_value=datetime.date.today())
        time = st.time_input("⏰ Janm ka samay (Birth Time):")
        place = st.text_input("📍 Janm Sthan (Birthplace):", placeholder="e.g., Delhi, Mumbai")

        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Generate Kundali ✨")
        with col2:
            back = st.form_submit_button("← Go Back")

    if back:
        st.session_state.page = "home"
        st.rerun()

    if submit:
        if name and place:
            with st.spinner("Analyzing Stars and Planets..."):
                url = "https://api.freeastroapi.com/api/v1/natal/calculate"
                payload = {
                    "year": dob.year, "month": dob.month, "day": dob.day,
                    "hour": time.hour, "minute": time.minute, "city": place
                }
                headers = {"Content-Type": "application/json", "x-api-key": API_KEY}

                try:
                    response = requests.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        st.session_state.user_data = {
                            "name": name,
                            "dob": dob.strftime('%d %b %Y'),
                            "time": time.strftime('%I:%M %p'),
                            "place": place,
                            "api_data": response.json() 
                        }
                        st.session_state.page = "result"
                        st.rerun()
                    else:
                        st.error(f"API Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Bhai, Naam aur Janm Sthan bharna zaroori hai!")

# --- PAGE 3: RESULT ---
elif st.session_state.page == "result":
    data = st.session_state.user_data
    
    # --- HEADER CARD ---
    st.markdown(f"""
        <div class="glass-card">
            <h2>🌟 Kundali Report 🌟</h2>
            <h3 style='color: #ff7676 !important;'>{data['name']}</h3>
            <p>📅 {data['dob']} | ⏰ {data['time']} | 📍 {data['place']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # --- GRAPH & PLANETS SECTION ---
    st.markdown("<h3 style='text-align: left;'>🪐 Grah Dasha & Rashiyan</h3>", unsafe_allow_html=True)
    
    # API response se planets ka data nikalna
    planets_data = data['api_data'].get('planets', [])
    
    if planets_data:
        # Planets ko 2 columns mein dikhane ke liye
        cols = st.columns(2)
        
        for index, planet in enumerate(planets_data):
            p_name = planet.get('name', 'Unknown')
            p_sign = planet.get('sign', 'Unknown')
            p_degree = planet.get('pos', 0)
            is_retro = planet.get('retrograde', False)
            
            # Graho ke naam ke emojis
            emojis = {"Sun": "☀️", "Moon": "🌙", "Mercury": "☿️", "Venus": "♀️", 
                      "Mars": "♂️", "Jupiter": "♃", "Saturn": "♄", "Rahu": "☊", "Ketu": "☋"}
            emoji = emojis.get(p_name, "🌟")
            
            # Retrograde (Vakri) check
            retro_text = " (Vakri 🔄)" if is_retro else ""
            
            # Card Design
            card_html = f"""
            <div style="background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #ff4b4b;">
                <h4 style="margin: 0; color: #fff;">{emoji} {p_name}</h4>
                <p style="margin: 5px 0 0 0; color: #ccc; font-size: 16px;">
                    Rashi: <b>{p_sign}</b>{retro_text}<br>
                    Degree: {p_degree}°
                </p>
            </div>
            """
            
            # 2 columns mein alternate karke daalna
            with cols[index % 2]:
                st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.error("Kundali ka data nahi mila.")

    st.write("")
    st.write("")
    
    # --- BACK BUTTON ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Check Another Kundali"):
            st.session_state.page = "home"
            st.session_state.user_data = {}
            st.rerun()