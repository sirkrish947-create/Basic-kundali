import streamlit as st
import datetime

# Page ki setting (Title aur Icon)
st.set_page_config(page_title="Kundali Analyzer", page_icon="🔮", layout="centered")

# Custom CSS (Design thoda sundar karne ke liye)
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 50px;
        width: 100%;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Heading
st.title("🔮 Astro Kundali Generator")
st.write("Apni details bharein aur apni basic kundali ka analysis dekhein. (Demo Version)")

st.divider() # Ek line design ke liye

# Form banate hain taaki ek saath data mile
with st.form("kundali_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 Apna Naam likhein:")
        dob = st.date_input("📅 Date of Birth:", min_value=datetime.date(1950, 1, 1), max_value=datetime.date.today())
    
    with col2:
        time = st.time_input("⏰ Janm ka samay (Birth Time):")
        place = st.text_input("📍 Janm Sthan (Birthplace):", placeholder="e.g., Delhi, Mumbai")

    # Submit Button
    submit = st.form_submit_button("Kundali Nikalein ✨")

# Agar user button dabata hai
if submit:
    if name and place:
        st.success(f"Namaste **{name}**! Aapki details mil gayi hain.")
        
        # Zodiac Sign nikalne ka logic (Date of Birth ke hisaab se)
        day = dob.day
        month = dob.month
        
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            sun_sign = "Mesh (Aries) ♈"
            element = "Agni (Fire)"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            sun_sign = "Vrishabh (Taurus) ♉"
            element = "Prithvi (Earth)"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            sun_sign = "Mithun (Gemini) ♊"
            element = "Vayu (Air)"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            sun_sign = "Kark (Cancer) ♋"
            element = "Jal (Water)"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            sun_sign = "Simha (Leo) ♌"
            element = "Agni (Fire)"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            sun_sign = "Kanya (Virgo) ♍"
            element = "Prithvi (Earth)"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            sun_sign = "Tula (Libra) ♎"
            element = "Vayu (Air)"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            sun_sign = "Vrishchik (Scorpio) ♏"
            element = "Jal (Water)"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            sun_sign = "Dhanu (Sagittarius) ♐"
            element = "Agni (Fire)"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            sun_sign = "Makar (Capricorn) ♑"
            element = "Prithvi (Earth)"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            sun_sign = "Kumbh (Aquarius) ♒"
            element = "Vayu (Air)"
        else:
            sun_sign = "Meen (Pisces) ♓"
            element = "Jal (Water)"

        st.divider()
        st.subheader("📜 Aapki Basic Report")
        
        # Result ko sundar tarike se dikhana
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric(label="Naam", value=name)
        col_res2.metric(label="Surya Rashi", value=sun_sign)
        col_res3.metric(label="Tatva (Element)", value=element)
        
        st.info(f"📅 **Aapka Janm:** {dob.strftime('%d %B %Y')} ko {time.strftime('%I:%M %p')} baje, {place} mein hua tha.")
        
        st.warning("⚠️ **Note:** Ye ek demo calculation hai. Professional Grah, Nakshatra aur Lagna ki calculation ke liye humein Astrology API connect karni hogi.")
        
    else:
        st.error("Bhai, 'Naam' aur 'Janm Sthan' bharna mat bhoolna!")
