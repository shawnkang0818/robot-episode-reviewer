from pathlib import Path
from datetime import datetime

import pandas as pd

REVIEWS_FILE = Path("data/reviews.csv")


def save_review(
    episode_name: str,
    outcome: str,
    failure_type: str,
    notes: str,
) -> None:
    review = {
        "episode_name": episode_name,
        "reviewed_at": datetime.now().isoformat(timespec="seconds"),
        "outcome": outcome,
        "failure_type": failure_type,
        "notes": notes,
    }

    new_row = pd.DataFrame([review])

    if REVIEWS_FILE.exists():
        existing_reviews = pd.read_csv(REVIEWS_FILE)
        updated_reviews = pd.concat(
            [existing_reviews, new_row],
            ignore_index=True,
        )
    else:
        updated_reviews = new_row

    updated_reviews.to_csv(REVIEWS_FILE, index=False)