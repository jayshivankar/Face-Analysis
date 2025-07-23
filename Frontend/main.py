# main.py

import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av
import numpy as np
from PIL import Image

st.set_page_config(page_title="🧠 Face Health Analyzer", layout="centered")
st.title("🧠 Face Health Analyzer")
st.caption("📷 Upload or capture your face to generate a health report.")

# Session state to hold captured image
if "captured_image" not in st.session_state:
    st.session_state["captured_image"] = None

# ---- Option 1: Upload Image ----
uploaded_file = st.file_uploader("📤 Upload a face image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)
    st.session_state["captured_image"] = np.array(image)

# ---- Option 2: Webcam Capture ----
st.markdown("---")
st.subheader("📷 Or capture from webcam")


class CaptureProcessor(VideoProcessorBase):
    def __init__(self) -> None:
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
        st.image(frame, caption="📸 Captured Frame", use_container_width=True)
        st.session_state["captured_image"] = frame

# ---- Generate Report ----
st.markdown("---")
if st.session_state["captured_image"] is not None:
    if st.button("🧾 Generate Report"):
        st.success("✅ Image captured and ready for analysis.")
        #
else:
    st.info("📌 Please upload or capture a face image to begin.")
