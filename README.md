# Robot Episode Review & Failure Logging Tool

A lightweight human-in-the-loop QA tool for reviewing robotics task episodes, classifying failures, and converting operator observations into structured data for engineering analysis.

## Why This Project

Robotics operators often observe failures before engineers do.

A report such as:

> "The robot failed."

may be enough to indicate that something went wrong, but it provides limited value for debugging, reproduction, trend analysis, or engineering handoff.

This project explores a more structured operator workflow.

Instead of recording only a generic failure note, the reviewer captures:

* Episode identity
* Task outcome
* Failure category
* Failure timestamp
* Expected behavior
* Observed behavior
* Reproducibility
* Operator notes

The goal is to turn human observation into consistent, searchable, and analyzable QA data.

---

## Current Features

### Local Episode Playback

The application automatically discovers supported video files stored in the local `episodes/` directory.

Supported formats currently include:

* MP4
* MOV

The selected episode can be played directly inside the Streamlit interface.

---

### Stable Episode IDs

Each episode receives a normalized ID based on its filename.

For example:

```text
luke_snowboard 1.mp4
```

becomes:

```text
LUKE_SNOWBOARD_1
```

The normalization process removes inconsistent spaces and special characters so episode records can be referenced more reliably.

---

### Structured Episode Outcomes

Each reviewed episode is assigned a high-level outcome:

```text
SUCCESS
FAILURE
ABORTED
```

Outcome is intentionally separated from failure classification.

For example:

```text
Outcome: FAILURE
Failure Type: VISION_FAILURE
```

This allows overall task success statistics and specific failure categories to be analyzed independently.

---

### Failure Classification

Current failure categories include:

```text
NONE
GRASP_FAILURE
VISION_FAILURE
COLLISION
TIMEOUT
OPERATOR_ERROR
SYSTEM_ERROR
OTHER
```

The taxonomy is intentionally simple for the current version and can be extended as the project evolves.

---

### Engineering-Oriented Failure Reporting

For failed episodes, reviewers can capture:

* Failure timestamp in seconds
* Expected behavior
* Observed behavior
* Reproducibility
* Additional operator notes

Example:

```text
Episode ID:
LUKE_SNOWBOARD_1

Outcome:
FAILURE

Failure Type:
VISION_FAILURE

Failure Timestamp:
8.7 seconds

Expected Behavior:
Tracking system should maintain the subject near the center of the frame.

Observed Behavior:
Subject moved toward the right edge of the frame and tracking was lost.

Reproducibility:
UNKNOWN

Notes:
Video used as synthetic episode data for workflow testing.
```

This structure encourages reviewers to distinguish direct observation from assumptions about root cause.

---

## Data Validation

The application currently enforces several basic consistency rules.

Examples:

```text
SUCCESS + NONE
Valid

SUCCESS + COLLISION
Invalid

FAILURE + GRASP_FAILURE
Valid

FAILURE + NONE
Invalid
```

Failed episodes must also include an observed behavior description.

These checks help prevent contradictory or low-information records from entering the dataset.

---

## Review Persistence

Reviews are stored locally in:

```text
data/reviews.csv
```

Each record currently contains:

```text
episode_id
episode_name
reviewed_at
outcome
failure_type
failure_time_seconds
expected_behavior
observed_behavior
reproducibility
notes
```

For the current V1 design, each episode has one active review.

If an episode is reviewed again, its existing record is replaced with the latest review instead of creating an unintended duplicate.

This keeps the dataset aligned with the current episode-review workflow while leaving room for future version history or audit logging.

---

## Example Data Flow

```text
Episode Video
     |
     v
Operator Review
     |
     v
Outcome Classification
     |
     v
Failure Classification
     |
     v
Expected vs. Observed Behavior
     |
     v
Structured QA Record
     |
     v
CSV Dataset
```

The central idea is:

```text
Human Observation
        +
Structured Metadata
        =
Engineering-Usable QA Data
```

---

## Technology Stack

* Python
* Streamlit
* Pandas
* CSV
* pathlib

---

## Project Structure

```text
robot-episode-reviewer/
│
├── app.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── .gitkeep
│
└── episodes/
    └── .gitkeep
```

Episode videos and generated review CSV files are intentionally excluded from Git tracking.

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/shawnkang0818/robot-episode-reviewer.git
cd robot-episode-reviewer
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add a test episode

Place an `.mp4` or `.mov` file inside:

```text
episodes/
```

### 6. Start the application

```bash
streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

---

## Data Privacy

Video episodes and generated review datasets are not committed to the public repository.

The `.gitignore` excludes:

```text
episodes/*.mp4
episodes/*.mov
data/*.csv
```

This is especially important for future robotics workflows where episode recordings, logs, or operational data may contain proprietary or sensitive information.

The current development dataset uses synthetic or non-robotics video strictly for workflow demonstration.

---

## Design Decisions

### Why CSV Instead of a Database?

The current project focuses on the operator-to-engineering QA workflow rather than database architecture.

CSV provides:

* Simple persistence
* Easy inspection
* Easy export
* Compatibility with Python, spreadsheets, SQL ingestion, and analytics tools
* Minimal infrastructure for an early prototype

A database can be introduced later if the project requires concurrent reviewers, larger datasets, authentication, review history, or remote deployment.

### Why Separate Outcome From Failure Type?

`Outcome` describes whether the task succeeded.

`Failure Type` describes what kind of failure occurred.

Keeping them separate produces cleaner data and makes later analysis more flexible.

### Why Separate Expected and Observed Behavior?

Good technical reporting distinguishes:

```text
What should have happened
```

from:

```text
What actually happened
```

This makes operator reports more useful for reproduction and engineering investigation while reducing unsupported root-cause assumptions.

---

## Current Development Status

The project currently supports:

* Local episode discovery
* Video playback
* Episode ID generation
* Structured outcome classification
* Failure classification
* Failure timestamps
* Expected vs. observed behavior
* Reproducibility status
* Operator notes
* Input validation
* CSV persistence
* Updating existing episode reviews

The project is under active development.

---

## Planned Next Steps

Near-term development includes:

* Review queue and completion status
* Reviewed vs. unreviewed episode tracking
* Episode review progress metrics
* Success-rate analytics
* Failure-category statistics
* Failure filtering
* Engineering escalation flags
* Severity levels
* CSV export improvements
* Automated tests
* UI cleanup and portfolio screenshots

---

## Long-Term Direction

Possible future extensions include:

* Multiple reviewers
* Review history and audit trails
* Database-backed storage
* Robot log integration
* Automatic episode metadata extraction
* Frame-level annotations
* Failure clips
* Engineering triage queues
* Dataset-quality checks
* Automated analytics
* Robotics telemetry synchronization

The broader goal is to explore how operators can contribute not only through task execution, but also through high-quality observation, structured QA data, debugging support, and lightweight engineering tooling.

---

## Project Goal

This project is intended as a practical exploration of the bridge between:

```text
Robotics Operations
        |
        v
Quality Assurance
        |
        v
Structured Data
        |
        v
Engineering Feedback
        |
        v
Tooling and Automation
```

It demonstrates how an operator-oriented workflow can produce higher-quality information for robotics engineering teams.
