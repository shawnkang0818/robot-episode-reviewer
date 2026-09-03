import streamlit as st
from pathlib import Path
from storage import get_episode_id, save_review

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
    episode_id = get_episode_id(selected_video.name)

    st.caption(f"Episode ID: {episode_id}")

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

failure_time_seconds = st.number_input(
    "Failure Timestamp (seconds)",
    min_value=0.0,
    step=0.1,
    format="%.1f",
)

expected_behavior = st.text_area(
    "Expected Behavior",
    placeholder="What should the robot have done?",
)

observed_behavior = st.text_area(
    "Observed Behavior",
    placeholder="What did the robot actually do?",
)

reproducibility = st.selectbox(
    "Reproducibility",
    [
        "UNKNOWN",
        "YES",
        "NO",
    ],
)

notes = st.text_area(
    "Operator Notes",
    placeholder="Describe what happened during the episode.",
)

if st.button("Submit Review"):
    if outcome == "SUCCESS" and failure_type != "NONE":
        st.error("Successful episodes must use Failure Type = NONE.")

    elif outcome == "FAILURE" and failure_type == "NONE":
        st.error("Failed episodes must include a failure type.")

    elif outcome == "FAILURE" and not observed_behavior.strip():
        st.error("Failed episodes must include observed behavior.")

    else:
        save_review(
            episode_name=selected_video.name,
            outcome=outcome,
            failure_type=failure_type,
            failure_time_seconds=failure_time_seconds,
            expected_behavior=expected_behavior,
            observed_behavior=observed_behavior,
            reproducibility=reproducibility,
            notes=notes,
        )

        st.success("Review saved successfully.")