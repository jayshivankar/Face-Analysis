import streamlit as st
from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
import av
import cv2
import numpy as np
from PIL import Image
import tempfile

st.set_page_config(page_title="🧠 Face Health Analyzer", layout="centered")
st.title("🧠 Face Health Analyzer")
st.caption("📷 Upload or capture your face to generate a health report.")

# Session state to store images
if "captured_image" not in st.session_state:
    st.session_state["captured_image"] = None\

# upload option
uploaded_file = st.file_uploader("📤 Upload a face image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image,caption = "🖼️ Uploaded Image", use_column_width=True)
    st.session_state["captured_image"] = np.array(image)

# webcam option
