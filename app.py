import streamlit as st
import pandas as pd
import joblib


model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(page_title="Mobile Overheating Prediction", layout="centered")

st.title("📱 Mobile Overheating Prediction")
st.write("Enter phone usage details to predict overheating")


cpu_usage = st.slider("CPU Usage (%)", 0, 100, 30)
ram_usage = st.slider("RAM Usage (%)", 0, 100, 40)
brightness = st.slider("Screen Brightness (%)", 0, 100, 50)
screen_on_time = st.slider("Screen ON Time (hours)", 0.0, 8.0, 2.0)
apps_running = st.slider("Number of Apps Running", 0, 50, 5)
ambient_temp = st.slider("Ambient Temperature (°C)", 15, 45, 28)

device_state = st.selectbox(
    "Device State",
    ["Idle", "Normal Use", "Video Streaming", "Gaming"]
)

network_type = st.selectbox(
    "Network Type",
    ["WiFi", "5G", "4G"]
)

charging = st.radio("Charging", ["Yes", "No"])



device_state_idle = 1 if device_state == "Idle" else 0
device_state_normal_use = 1 if device_state == "Normal Use" else 0
device_state_video_streaming = 1 if device_state == "Video Streaming" else 0


network_type_5g = 1 if network_type == "5G" else 0
network_type_wifi = 1 if network_type == "WiFi" else 0


charging_yes = 1 if charging == "Yes" else 0



input_data = pd.DataFrame([[
    cpu_usage,
    ram_usage,
    brightness,
    screen_on_time,
    apps_running,
    ambient_temp,
    device_state_idle,
    device_state_normal_use,
    device_state_video_streaming,
    network_type_5g,
    network_type_wifi,
    charging_yes
]], columns=[
    'cpu_usage', 'ram_usage', 'brightness', 'screen_on_time',
    'apps_running', 'ambient_temp',
    'device_state_idle', 'device_state_normal_use', 'device_state_video_streaming',
    'network_type_5g', 'network_type_wifi', 'charging_yes'
])



if st.button("🔍 Predict"):
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]

    if prediction == 1:
        st.error("🔥 Overheating Detected!")
    else:
        st.success("✅ Normal Temperature (No Overheating)")