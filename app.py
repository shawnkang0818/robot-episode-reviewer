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

st.subheader("Episode Review")

outcome = st.selectbox(
    "Outcome",
    [
        "SUCCESS",
        "FAILURE",
        "ABORTED",
    ],
)

failure_type = st.selectbox(
    "Failure Type",
    [
        "NONE",
        "GRASP_FAILURE",
        "VISION_FAILURE",
        "COLLISION",
        "TIMEOUT",
        "OPERATOR_ERROR",
        "SYSTEM_ERROR",
        "OTHER",
    ],
)

notes = st.text_area(
    "Operator Notes",
    placeholder="Describe what happened during the episode.",
)

if st.button("Submit Review"):
    if outcome == "SUCCESS" and failure_type != "NONE":
        st.error("Successful episodes must use Failure Type = NONE.")
    else:
        st.success("Review is valid.")
        
    st.write("Selected episode:", selected_video.name)
    st.write("Outcome:", outcome)
    st.write("Failure type:", failure_type)
    st.write("Notes:", notes)