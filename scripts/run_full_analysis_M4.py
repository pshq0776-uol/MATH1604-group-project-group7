"""
run_full_analysis_M4.py
=======================
Integration script for the MATH1604 Python Quiz Response Analysis project.

Author: Danish Imran Agus Bin Faisal
Student ID: 202023762
Role: Team Member 4 (Team Leader)

Usage
-----
    python run_full_analysis_M4.py
"""

import os
import sys

# ── Constants ────────────────────────────────────────────────────────────────

BASE_URL = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
TOTAL_RESPONDENTS = 70
DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"
COLLATED_FILE = os.path.join(OUTPUT_FOLDER, "collated_answers.txt")

# ── Imports ──────────────────────────────────────────────────────────────────

try:
    from data_extraction_M1 import extract_answers_sequence, write_answers_sequence
    print("[M4] Successfully imported data_extraction_M1.")
except ImportError as e:
    print(f"[M4] ERROR: Could not import data_extraction_M1: {e}")
    sys.exit(1)

try:
    from data_preparation_M2 import download_answer_files, collate_answer_files
    print("[M4] Successfully imported data_preparation_M2.")
except ImportError as e:
    print(f"[M4] ERROR: Could not import data_preparation_M2: {e}")
    sys.exit(1)

try:
    from data_analysis_M3 import generate_means_sequence, visualize_data
    print("[M4] Successfully imported data_analysis_M3.")
except ImportError as e:
    print(f"[M4] ERROR: Could not import data_analysis_M3: {e}")
    sys.exit(1)

# ── Pipeline ─────────────────────────────────────────────────────────────────

def ensure_folders():
    """
    Create required output and data directories if they do not already exist.

    Returns
    -------
    None
    """
    os.makedirs(DATA_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"[M4] Directories ready: '{DATA_FOLDER}/', '{OUTPUT_FOLDER}/'")


def step1_download():
    """
    Download all available respondent answer files from the cloud repository.

    Calls download_answer_files from data_preparation_M2 to retrieve up to
    TOTAL_RESPONDENTS files. Files that do not exist on the server are
    handled gracefully by the M2 module.

    Returns
    -------
    None
    """
    print(f"\n[M4] STEP 1: Downloading answer files (requesting {TOTAL_RESPONDENTS})...")
    download_answer_files(BASE_URL, DATA_FOLDER, TOTAL_RESPONDENTS)
    print("[M4] Download complete.")


def step2_collate():
    """
    Collate all downloaded respondent files into a single unified file.

    Calls collate_answer_files from data_preparation_M2 to merge all
    individual respondent files in the data/ folder into one
    collated_answers.txt in the output/ folder.

    Returns
    -------
    None
    """
    print("\n[M4] STEP 2: Collating answer files...")
    collate_answer_files(DATA_FOLDER)
    print(f"[M4] Collation complete. Output: '{COLLATED_FILE}'")


def step3_extract_and_write():
    """
    Extract and save individual answer sequences for all respondent files.

    Iterates over each respondent file in the data/ folder, applies
    extract_answers_sequence from data_extraction_M1, and saves the
    result using write_answers_sequence. Skips any files that cannot
    be parsed.

    Returns
    -------
    None
    """
    print("\n[M4] STEP 3: Extracting individual answer sequences...")
    data_files = sorted(
        f for f in os.listdir(DATA_FOLDER)
        if f.startswith("answers_respondent_") and f.endswith(".txt")
    )

    for fname in data_files:
        file_path = os.path.join(DATA_FOLDER, fname)
        try:
            n = int(fname.replace("answers_respondent_", "").replace(".txt", ""))
            answers = extract_answers_sequence(file_path)
            write_answers_sequence(answers, n, OUTPUT_FOLDER)
        except (ValueError, FileNotFoundError) as e:
            print(f"[M4] WARNING: Skipping {fname} — {e}")

    print("[M4] Extraction complete.")


def step4_analyse():
    """
    Compute and display the mean answer value per question.

    Calls generate_means_sequence from data_analysis_M3 using the
    collated answers file and prints a summary of results.

    Returns
    -------
    None
    """
    print("\n[M4] STEP 4: Computing mean answer sequence...")
    means = generate_means_sequence(COLLATED_FILE)
    print(f"[M4] Means (first 10): {[round(m, 3) for m in means[:10]]}")

    unusual = [(i+1, round(m, 3)) for i, m in enumerate(means) if m < 1.8 or m > 3.2]
    if unusual:
        print(f"[M4] Questions with unusual means: {unusual[:10]}")
    else:
        print("[M4] No strongly unusual means detected.")


def step5_visualise():
    """
    Generate visualisations of the answer distributions.

    Calls visualize_data from data_analysis_M3 twice:
    - n=1: scatter plot of means per question
    - n=2: line plot of all individual respondent answer sequences

    Returns
    -------
    None
    """
    print("\n[M4] STEP 5: Generating visualisations...")
    print("[M4] Plot 1: Scatter plot of means...")
    visualize_data(COLLATED_FILE, 1)
    print("[M4] Plot 2: Line plot of all respondent sequences...")
    visualize_data(COLLATED_FILE, 2)
    print("[M4] Visualisation complete.")


def main():
    """
    Execute the full analysis pipeline in sequence.

    Steps:
        1. Ensure required directories exist.
        2. Download raw answer files from the cloud.
        3. Collate downloaded files into one unified file.
        4. Extract and save individual answer sequences.
        5. Compute statistical means per question.
        6. Generate visualisations.

    Returns
    -------
    None
    """
    print("=" * 60)
    print("  MATH1604 — Python Quiz Response Analysis Pipeline")
    print("=" * 60)

    ensure_folders()
    step1_download()
    step2_collate()
    step3_extract_and_write()
    step4_analyse()
    step5_visualise()

    print("\n[M4] Full pipeline complete.")


if __name__ == "__main__":
    main()
