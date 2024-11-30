import streamlit as st
import requests
from PIL import Image
import io

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

# Streamlit App Customization
st.set_page_config(
    page_title="Text-to-Image Generator",
    page_icon="🎨",
    layout="wide",
)

# App Title
st.title("🎨 Text-to-Image Generator with History")
st.markdown("Generate and revisit stunning AI-generated images! 🚀")

# Sidebar: Service Status
st.sidebar.header("Service Status")
try:
    health_response = requests.get(f"{API_URL}/health")
    if health_response.status_code == 200:
        health_status = health_response.json()
        st.sidebar.success(f"✅ {health_status['status']} on {health_status['device'].upper()}")
    else:
        st.sidebar.error("❌ Service is unavailable.")
except requests.exceptions.RequestException:
    st.sidebar.error("❌ Failed to connect to the backend.")

# Generate New Image
st.markdown("### 📝 Generate a New Image:")
prompt = st.text_input("", placeholder="E.g., A futuristic cityscape at sunset 🌃")
generate_button = st.button("✨ Generate Image")

if generate_button:
    if prompt.strip():
        with st.spinner("Generating image... ⏳"):
            try:
                response = requests.get(f"{API_URL}/generate", params={"prompt": prompt})
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Generated Image", use_column_width=True)
                else:
                    st.error("⚠️ Failed to generate the image.")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("⚠️ Please enter a prompt.")

# Display History
st.markdown("### 🗂️ Prompt History:")
try:
    history_response = requests.get(f"{API_URL}/history")
    if history_response.status_code == 200:
        history = history_response.json()
        if history:
            for entry in history:
                st.markdown(f"**Prompt:** {entry['prompt']}")
                st.image(entry["image_path"], caption=f"Generated from: {entry['prompt']}", use_column_width=True)
        else:
            st.info("No history found.")
    else:
        st.error("⚠️ Failed to fetch history.")
except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Error: {e}")
