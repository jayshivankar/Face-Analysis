import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoProcessorBase
import av
import numpy as np
from PIL import Image
import io
import cv2
import os

# --- Internal imports ---
# from facial_symmetry import analyze_symmetry
# from age_gender_prediction import predict_age_gender
# from fatigue_prediction import predict_fatigue
# from skin_disease_classifier import predict_skin_disease
# from utils import extract_cheek_region

st.set_page_config(page_title="🧠 Face Health Analyzer", layout="centered")
st.title("🧠 Face Health Analyzer")
st.caption("📷 Upload or capture your face to generate a health report.")

# --- Session state ---
if "captured_image" not in st.session_state:
    st.session_state["captured_image"] = None
if "skin_image" not in st.session_state:
    st.session_state["skin_image"] = None

# --- Upload image ---
st.subheader("🖼️ Upload a face image")
uploaded_file = st.file_uploader("Upload a frontal face image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)
    st.session_state["captured_image"] = np.array(image)

# --- Webcam capture ---
st.markdown("---")
st.subheader("📷 Or capture from webcam")

class CaptureProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.frame = img
        return frame

ctx = webrtc_streamer(
    key="capture",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=CaptureProcessor,
)

if ctx.video_processor and st.button("📸 Capture Frame"):
    frame = ctx.video_processor.frame
    if frame is not None:
        st.image(frame, caption="Captured Frame", use_container_width=True)
        st.session_state["captured_image"] = frame

# --- Upload skin image ---
st.markdown("---")
st.subheader("🔍 Upload a close-up of the skin area (e.g., cheek, chin, forehead)")
skin_file = st.file_uploader("Upload zoomed-in skin image (optional)", type=["jpg", "jpeg", "png"])
if skin_file:
    skin_img = Image.open(skin_file).convert("RGB")
    st.image(skin_img, caption="Uploaded Skin Area", use_container_width=True)
    st.session_state["skin_image"] = np.array(skin_img)

# --- Generate Report ---
st.markdown("---")
if st.session_state["captured_image"] is not None:
    if st.button("🧾 Generate Report"):
        face_image = st.session_state["captured_image"]

        st.subheader("📊 Analysis Report")
        with st.spinner("Predicting age and gender..."):
            age, gender = predict_age_gender(face_image)
            st.write(f"Age: {age}", f"Gender: {gender}")

        with st.spinner("Analyzing facial symmetry..."):
            result = analyze_symmetry(face_image)
            st.write(f"Facial Symmetry: {result}")

        with st.spinner("Predicting fatigue..."):
            fatigue = predict_fatigue(face_image)
            st.write(f"Fatigue Status: {fatigue}")

        # Handle skin image
        skin_input = st.session_state["skin_image"]
        if skin_input is None:
            with st.spinner("Trying to extract cheek region for skin analysis..."):
                cheek_crop = extract_cheek_region(face_image)
                if cheek_crop is not None:
                    skin_input = cheek_crop
                    st.image(skin_input, caption="Auto-extracted cheek region", use_container_width=True)
                else:
                    st.warning("Could not auto-extract a valid skin region. Please upload a close-up.")

        if skin_input is not None:
            with st.spinner("Running skin disease classifier..."):
                disease = predict_skin_disease(skin_input)
                st.success(f"Detected Skin Condition: {disease}")

else:
    st.info("📌 Please upload or capture a face image to begin.")
