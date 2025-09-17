# main.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av
from PIL import Image
import numpy as np
import cv2
import os

# --- Internal imports ---
from facial_symmetry import analyze_symmetry, draw_landmarks
from analyzers import predict_age_gender, predict_fatigue, predict_skin_disease

# --- Page Config ---
st.set_page_config(page_title="🧠 Face Health Analyzer", layout="centered")
st.title("🧠 Face Health Analyzer")
st.caption("📷 Upload or capture your face to generate a personalized health report.")

# --- Session state ---
if "captured_image" not in st.session_state:
    st.session_state["captured_image"] = None
if "skin_image" not in st.session_state:
    st.session_state["skin_image"] = None
if "last_report" not in st.session_state:
    st.session_state["last_report"] = None

# --- Model status ---
st.sidebar.header("Model Status")
from analyzers import age_model, gender_model, fatigue_model, skin_model

model_status = {
    "Age Model": "✅ Loaded" if age_model else "❌ Not Loaded",
    "Gender Model": "✅ Loaded" if gender_model else "❌ Not Loaded",
    "Fatigue Model": "✅ Loaded" if fatigue_model else "❌ Not Loaded",
    "Skin Model": "✅ Loaded" if skin_model else "❌ Not Loaded"
}

for model, status in model_status.items():
    st.sidebar.write(f"{model}: {status}")

# --- Upload face image ---
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
st.subheader("🔍 Upload a close-up of the skin area")
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

        # Age & Gender
        with st.spinner("Predicting age and gender..."):
            age, gender = predict_age_gender(face_image)
        st.success(f"👤 **Predicted Age:** {age} years | **Gender:** {gender}")

        # Symmetry
        with st.spinner("Analyzing facial symmetry..."):
            symmetry = analyze_symmetry(face_image)
        if "error" in symmetry:
            st.error(symmetry["error"])
        else:
            st.info(f"🔄 **Asymmetry Score:** {symmetry['asymmetry_score']}")
            st.write(f"🧾 **Condition:** {symmetry['predicted_condition']}")

            # Show landmark visualization
            st.subheader("Facial Landmarks")
            annotated_image = draw_landmarks(face_image)
            st.image(annotated_image, caption="Facial Landmarks Detection", use_container_width=True)

        # Fatigue
        with st.spinner("Predicting fatigue..."):
            fatigue = predict_fatigue(face_image)
        if "Fatigued" in fatigue:
            st.error(f"😴 **Fatigue Status:** {fatigue}")
        else:
            st.success(f"⚡ **Fatigue Status:** {fatigue}")

        # Skin analysis
        skin_input = st.session_state["skin_image"]
        if skin_input is not None:
            with st.spinner("Running skin disease classifier..."):
                disease = predict_skin_disease(skin_input)
            if "Normal" in disease or "Uncertain" in disease:
                st.success(f"✨ **Skin Condition:** {disease}")
            else:
                st.warning(f"⚠️ **Detected Skin Condition:** {disease}")
        else:
            st.info("No skin image provided. Skin analysis skipped.")

        # Save report to session
        st.session_state["last_report"] = {
            "age": age,
            "gender": gender,
            "symmetry": symmetry,
            "fatigue": fatigue,
            "disease": disease if skin_input is not None else "Not analyzed",
        }

# --- Download Report ---
if st.session_state["last_report"] is not None:
    report_data = st.session_state["last_report"]
    report = f"""
Face Health Report
-----------------
Age: {report_data['age']}
Gender: {report_data['gender']}
Symmetry Score: {report_data['symmetry'].get('asymmetry_score', 'N/A')}
Condition: {report_data['symmetry'].get('predicted_condition', 'N/A')}
Fatigue: {report_data['fatigue']}
Skin Condition: {report_data['disease']}

Disclaimer: This analysis is for informational purposes only and is not a substitute for professional medical advice.
"""
    st.download_button("⬇️ Download Report", report, file_name="face_report.txt")

# --- Disclaimer ---
st.markdown("---")
st.markdown("""
**Disclaimer:** This application provides health-related information for educational purposes only. 
It is not a substitute for professional medical advice, diagnosis, or treatment. 
Always seek the advice of qualified healthcare providers with questions about medical conditions.
""")