from pathlib import Path
from datetime import datetime

import pandas as pd
import re

REVIEWS_FILE = Path("data/reviews.csv")


def save_review(
    episode_name: str,
    outcome: str,
    failure_type: str,
    failure_time_seconds: float,
    expected_behavior: str,
    observed_behavior: str,
    reproducibility: str,
    notes: str,
) -> None:
    episode_id = get_episode_id(episode_name)

    review = {
        "episode_id": episode_id,
        "episode_name": episode_name,
        "reviewed_at": datetime.now().isoformat(timespec="seconds"),
        "outcome": outcome,
        "failure_type": failure_type,
        "failure_time_seconds": failure_time_seconds,
        "expected_behavior": expected_behavior,
        "observed_behavior": observed_behavior,
        "reproducibility": reproducibility,
        "notes": notes,
    }

    new_row = pd.DataFrame([review])

    if REVIEWS_FILE.exists():
        existing_reviews = pd.read_csv(REVIEWS_FILE)

        existing_reviews = existing_reviews[
            existing_reviews["episode_id"] != episode_id
        ]

        updated_reviews = pd.concat(
            [existing_reviews, new_row],
            ignore_index=True,
        )
    else:
        updated_reviews = new_row

    updated_reviews.to_csv(REVIEWS_FILE, index=False)

def get_episode_id(episode_name: str) -> str:
    stem = Path(episode_name).stem.upper()
    normalized = re.sub(r"[^A-Z0-9]+", "_", stem)
    return normalized.strip("_")