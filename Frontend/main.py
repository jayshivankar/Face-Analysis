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