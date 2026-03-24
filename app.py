import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI App 💙", layout="wide")

# -------- BLUE THEME CSS --------
st.markdown("""
    <style>
    .stApp {
        background-color: #e6f2ff;
    }

    button[data-baseweb="tab"] {
        color: #003366 !important;
        font-weight: bold;
        font-size: 16px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 3px solid #003366 !important;
        color: #003366 !important;
    }

    h1, h2, h3 {
        color: #003366 !important;
    }

    .stMarkdown {
        color: #003366 !important;
    }

    .stButton>button {
        background-color: #3399ff;
        color: white;
        border-radius: 10px;
        height: 45px;
        width: 100%;
    }

    .stFileUploader {
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------- TITLE --------
st.markdown("<h1> AI Selfie & Video Classifier 💙</h1>", unsafe_allow_html=True)
st.write("Upload multiple images and videos together 🎯")

# -------- TABS --------
tab1, tab2 = st.tabs(["📸 Multiple Images", "🎥 Multiple Videos"])

# ================= IMAGE SECTION =================
with tab1:
    st.subheader("Upload Multiple Images")

    image_files = st.file_uploader(
        "Choose Images",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if image_files:
        for img_file in image_files:
            col1, col2 = st.columns(2)

            img = Image.open(img_file)
            img_array = np.array(img)

            with col1:
                st.markdown(f"### 📸 {img_file.name}")
                st.image(img, width=180)

            # Example processing (replace with ML model)
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

            with col2:
                st.markdown("### 🤖 Output")
                st.image(gray, width=180)

            st.success(f"{img_file.name} processed ✅")
            st.markdown("---")

# ================= VIDEO SECTION =================
with tab2:
    st.subheader("Upload Multiple Videos")

    video_files = st.file_uploader(
        "Choose Videos",
        type=["mp4", "avi", "mov"],
        accept_multiple_files=True
    )

    if video_files:
        for vid_file in video_files:

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### 🎥 {vid_file.name}")
                st.video(vid_file)  # smaller area due to column

            with col2:
                st.write("Processing...")

                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(vid_file.read())

                cap = cv2.VideoCapture(tfile.name)
                frame_count = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_count += 1

                    # Show fewer frames (clean UI)
                    if frame_count % 50 == 0:
                        frame = cv2.resize(frame, (200, 150))  # SMALL SIZE
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        st.image(frame, width=200)

                cap.release()

            st.success(f"{vid_file.name} processed 🎉")
            st.markdown("---")
# -------- FOOTER --------
st.markdown("---")
st.markdown("<p style='text-align:center;color:#003366;'>Made with using Streamlit</p>", unsafe_allow_html=True)