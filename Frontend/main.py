# main.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import numpy as np
from PIL import Image

st.set_page_config(page_title="🧠 Face Health Analyzer", layout="centered")
st.title("🧠 Face Health Analyzer")
st.caption("📷 Upload or capture your face to generate a health report.")

# Session state to store image
if "captured_image" not in st.session_state:
    st.session_state["captured_image"] = None

# ---- Upload Option ----
uploaded_file = st.file_uploader("📤 Upload a face image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)
    st.session_state["captured_image"] = np.array(image)

# ---- Webcam Option ----
st.markdown("---")
st.subheader("📷 Or capture photo from webcam")

class CaptureTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        image = frame.to_ndarray(format="bgr24")
        self.frame = image
        return image

ctx = webrtc_streamer(
    key="capture",
    video_transformer_factory=CaptureTransformer,
    media_stream_constraints={"video": True, "audio": False},
)

if ctx.video_transformer and st.button("📸 Capture Frame"):
    frame = ctx.video_transformer.frame
    if frame is not None:
        st.image(frame, caption="📸 Captured Image", use_column_width=True)
        st.session_state["captured_image"] = frame

# ---- Generate Report ----
st.markdown("---")
if st.session_state["captured_image"] is not None:
    if st.button("🧾 Generate Report"):
        st.success("✅ Image captured and ready for analysis.")
        # Actual processing will be handled elsewhere
else:
    st.info("📌 Please upload or capture a face image to begin.")
