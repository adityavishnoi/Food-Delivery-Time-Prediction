import pickle
import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SwiftDelivery | Vibrant ETA",
    page_icon="🌈",
    layout="centered"
)

# --- VIBRANT CSS INJECTION ---
st.markdown("""
    <style>
    /* Animated Vibrant Background */
    .stApp {
        background: linear-gradient(-45deg, #ff00cc, #3333ff, #00ffff, #ff9900);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Force all text inside the main block to be white for contrast */
    h1, h2, h3, p, label, .st-emotion-cache-10trnc {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.4);
    }

    /* Vibrant Glassmorphism Container */
    [data-testid="stForm"] {
        background: rgba(10, 15, 30, 0.65); /* Dark translucent glass */
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 30px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 3rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 
                    inset 0 0 20px rgba(255, 255, 255, 0.1);
    }

    /* Animated Glowing Rainbow Button */
    div.stButton > button {
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        background-size: 300%;
        animation: rainbowBG 4s linear infinite;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.5);
        padding: 16px 32px;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: 2px;
        border-radius: 50px;
        width: 100%;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.6), 
                    0 0 40px rgba(255, 0, 255, 0.6);
        transition: all 0.3s ease-in-out;
    }

    @keyframes rainbowBG {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* Extreme Glow on Hover */
    div.stButton > button:hover {
        transform: scale(1.03) translateY(-3px);
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.9), 
                    0 0 60px #00ffff, 
                    0 0 90px #ff00ff;
        border: 2px solid white;
    }

    div.stButton > button:active {
        transform: scale(0.98);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    /* Vibrant Result Dashboard */
    .glowing-result {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
        backdrop-filter: blur(30px);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.2);
        animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    
    .eta-text {
        font-size: 1.4rem;
        color: #f8fafc;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 10px;
        font-weight: 700;
    }

    .eta-time {
        font-size: 6rem;
        font-weight: 900;
        background: linear-gradient(to bottom right, #fff, #ffeb3b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
        text-shadow: 0px 0px 20px rgba(255, 235, 59, 0.5);
    }

    .eta-breakdown {
        margin-top: 25px;
        font-size: 1.3rem;
        color: #ffffff;
        font-weight: 600;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }

    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.8); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LOAD ASSETS ---
@st.cache_resource(show_spinner=False)
def load_assets():
    with open("best_rf_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("label_encoders.pkl", "rb") as f:
        encoders = pickle.load(f)
    return model, encoders

try:
    model, encoders = load_assets()
except FileNotFoundError:
    st.error("Missing `best_rf_model.pkl` or `label_encoders.pkl`.")
    st.stop()

# --- HEADER ---
st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0; text-transform: uppercase; letter-spacing: 4px;'>🚀 Delivery Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.4rem; margin-bottom: 2rem; font-weight: bold;'>Real-Time AI Predictions</p>", unsafe_allow_html=True)

# --- VIBRANT FORM ---
with st.form("prediction_form", border=False):
    
    st.markdown("<h3>📍 Order Routing</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        distance_km = st.slider("Route Distance (km)", 0.5, 30.0, 5.0, 0.5)
    with col2:
        prep_time = st.slider("Prep Time (min)", 5, 90, 15, 1)

    st.markdown("<br><h3>🌤️ Live Conditions</h3>", unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3)
    with col3:
        weather = st.selectbox("Weather", options=list(encoders["Weather"].classes_))
    with col4:
        traffic = st.selectbox("Traffic Level", options=list(encoders["Traffic_Level"].classes_))
    with col5:
        time_of_day = st.selectbox("Time of Day", options=list(encoders["Time_of_Day"].classes_))

    st.markdown("<br><h3>🛵 Courier Assignment</h3>", unsafe_allow_html=True)
    col6, col7 = st.columns(2)
    with col6:
        vehicle_type = st.selectbox("Vehicle Type", options=list(encoders["Vehicle_Type"].classes_))
    with col7:
        courier_exp = st.slider("Courier Experience (Yrs)", 0.0, 15.0, 2.0, 0.5)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Animated Rainbow Glowing Button
    submitted = st.form_submit_button("🔥 PREDICT ETA NOW 🔥")

# --- RESULTS ---
if submitted:
    with st.spinner("✨ Analyzing logistics..."):
        time.sleep(0.6)

    # Encoding
    encoded_weather = encoders["Weather"].transform([weather])[0]
    encoded_traffic = encoders["Traffic_Level"].transform([traffic])[0]
    encoded_time = encoders["Time_of_Day"].transform([time_of_day])[0]
    encoded_vehicle = encoders["Vehicle_Type"].transform([vehicle_type])[0]

    input_data = pd.DataFrame([{
        "Distance_km": distance_km,
        "Weather": encoded_weather,
        "Traffic_Level": encoded_traffic,
        "Time_of_Day": encoded_time,
        "Vehicle_Type": encoded_vehicle,
        "Preparation_Time_min": prep_time,
        "Courier_Experience_yrs": courier_exp
    }])

    # Predict
    predicted_eta = model.predict(input_data)[0]
    transit_time = predicted_eta - prep_time

    # Colorful Output UI
    st.markdown(f"""
        <div style="margin-top: 40px;">
            <div class="glowing-result">
                <div class="eta-text">Total Estimated Time</div>
                <h2 class="eta-time">{predicted_eta:.0f} MIN</h2>
                <div class="eta-breakdown">
                    🍔 Prep: {int(prep_time)}m &nbsp; ⏳ &nbsp; 🏍️ Transit: {transit_time:.0f}m
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.balloons()