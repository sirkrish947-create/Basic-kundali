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
    
    st.markdown(f"""
        <div class="glass-card">
            <h2>🌟 Kundali Report 🌟</h2>
            <h3 style='color: #ff7676 !important;'>{data['name']}</h3>
            <p>📅 {data['dob']} | ⏰ {data['time']} | 📍 {data['place']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.subheader("Planetary Positions (Raw API Data)")
    
    # Yahan hum API se aaya hua data dikha rahe hain
    # Jaise hi tumhe JSON ka screenshot dikhega, hum isko sundar cards mein badal denge
    st.json(data['api_data'])
    
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Check Another Kundali"):
            st.session_state.page = "home"
            st.session_state.user_data = {}
            st.rerun()
