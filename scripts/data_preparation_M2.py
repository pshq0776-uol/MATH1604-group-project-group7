"""
data_preparation_M2.py
======================
Module for downloading and collating Python quiz answer files.

Author: Zimo Wang
Student ID: 201939193
Role: Team Member 2
"""

import os
import urllib.request
import urllib.error
import requests
import logging
from typing import Optional, Tuple, List
DEFAULT_TIMEOUT = 10
RESPONDENT_PREFIX = "answers_respondent_"
FILE_SUFFIX = ".txt"
SEPARATOR_LINE = "*"
COLLATED_FILENAME = "collated_answers.txt"
OUTPUT_DIR = "output"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_answer_files(cloud_url: str, path_to_data_folder: str, total_respondents: int) -> None:
    """
    Download respondent answer files from a cloud location and save them locally.

    Attempts to download files named a1.txt, a2.txt, ..., aN.txt from the
    given base URL, where N is total_respondents. Each successfully downloaded
    file is saved into path_to_data_folder under a standardised name:
    answers_respondent_1.txt, answers_respondent_2.txt, etc.

    If a file does not exist on the server (e.g. because fewer files are
    published than requested), the HTTP 404 error is caught and logged, and
    the function continues with the next file.

    Parameters
    ----------
    cloud_url : str
        Base URL of the cloud repository (without trailing slash).
    path_to_data_folder : str
        Local path to the folder where downloaded files will be saved.
        The folder is created automatically if it does not already exist.
    total_respondents : int
        Number of files to attempt downloading (from a1.txt to aN.txt).

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If total_respondents is not a positive integer.

    Examples
    --------
    >>> download_answer_files(
    ...     'https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main',
    ...     'data',
    ...     70
    ... )
    """
    if not isinstance(total_respondents, int) or total_respondents <= 0:
        raise ValueError(
            f"total_respondents must be a positive integer, got: {total_respondents}"
        )

    os.makedirs(path_to_data_folder, exist_ok=True)

    downloaded = 0
    skipped = 0

    for n in range(1, total_respondents + 1):
        file_url = f"{cloud_url}/a{n}.txt"
        destination = os.path.join(path_to_data_folder, f"answers_respondent_{n}.txt")

        try:
            with urllib.request.urlopen(file_url) as response:
                content = response.read().decode('utf-8')

            with open(destination, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[M2] Downloaded: a{n}.txt → answers_respondent_{n}.txt")
            downloaded += 1

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"[M2] Not found (skipped): a{n}.txt — HTTP 404")
                skipped += 1
            else:
                print(f"[M2] HTTP error downloading a{n}.txt — {e.code}: {e.reason}")
                skipped += 1

        except urllib.error.URLError as e:
            print(f"[M2] Network error downloading a{n}.txt — {e.reason}")
            skipped += 1

    print(f"\n[M2] Download summary: {downloaded} downloaded, {skipped} skipped.")


def collate_answer_files(data_folder_path: str) -> None:
    """
    Combine all individual respondent answer files into one unified file.

    Reads every file named answers_respondent_N.txt from data_folder_path,
    ordered numerically by respondent ID, and writes their contents into a
    single file named collated_answers.txt in the output/ folder. Each
    respondent's section is separated by a line containing a single asterisk (*).

    Parameters
    ----------
    data_folder_path : str
        Path to the folder containing individual respondent files.

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        If data_folder_path does not exist.
    RuntimeError
        If no respondent files are found in data_folder_path.

    Examples
    --------
    >>> collate_answer_files('data')
    # Creates 'output/collated_answers.txt'
    """
    if not os.path.isdir(data_folder_path):
        raise FileNotFoundError(
            f"Data folder not found: '{data_folder_path}'"
        )

    all_files = []
    for fname in os.listdir(data_folder_path):
        if fname.startswith("answers_respondent_") and fname.endswith(".txt"):
            try:
                n = int(fname.replace("answers_respondent_", "").replace(".txt", ""))
                all_files.append((n, fname))
            except ValueError:
                pass

    if not all_files:
        raise RuntimeError(
            f"No respondent files found in '{data_folder_path}'. "
            "Run download_answer_files first."
        )

    all_files.sort(key=lambda x: x[0])

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "collated_answers.txt")

    with open(output_path, 'w', encoding='utf-8') as out_f:
        for i, (n, fname) in enumerate(all_files):
            file_path = os.path.join(data_folder_path, fname)

            with open(file_path, 'r', encoding='utf-8') as in_f:
                content = in_f.read()

            out_f.write(content)
            out_f.write("\n*\n")

            print(f"[M2] Collated: {fname}")

    print(f"\n[M2] Collation complete. {len(all_files)} files written to '{output_path}'.")
