import streamlit as st
from pathlib import Path

st.title("Robot Episode Review Tool")

st.write(
    "Review robotics task episodes, classify outcomes, "
    "and capture structured QA observations."
)

EPISODES_DIR = Path("episodes")

video_files = sorted(
    list(EPISODES_DIR.glob("*.mp4"))
    + list(EPISODES_DIR.glob("*.mov"))
)

if not video_files:
    st.info("No episode videos found. Add an MP4 or MOV file to the episodes folder.")
else:
    selected_video = st.selectbox(
        "Select an episode",
        video_files,
        format_func=lambda path: path.name,
    )

    st.video(str(selected_video))