"""
data_extraction_M1.py
=====================
Module for parsing Python quiz answer files and writing extracted sequences.

This module is part of the MATH1604 Group Project and implements the
data extraction layer of the analysis pipeline.

Author: Abdulaziz Aldawsari
Student ID: 202003156
Role: Team Member 1
"""

import os
import re


def extract_answers_sequence(file_path: str) -> list:
    """
    Parse a quiz answer text file and extract the respondent's answer sequence.

    Each question in the file has four answer options marked with square
    brackets. A selected answer is indicated by '[x]', and an unanswered
    question has all brackets empty '[ ]'. This function reads the file,
    identifies which option was selected for each question, and returns
    a list of integers representing the answers.

    Parameters
    ----------
    file_path : str
        Path to the quiz answers text file (e.g., 'data/a1.txt').

    Returns
    -------
    list of int
        A list of exactly 100 integers. Each value is:
        - 1, 2, 3, or 4 if the corresponding option was selected,
        - 0 if the question was left unanswered.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist at the given path.
    ValueError
        If the file does not contain exactly 100 questions.

    Examples
    --------
    >>> answers = extract_answers_sequence('data/a1.txt')
    >>> print(answers[:5])
    [1, 2, 0, 3, 4]
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Answer file not found: {file_path}")

    answers = []
    current_options = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if re.match(r'^Question\s+\d+\.', line):
                if current_options:
                    selected = _get_selected_option(current_options)
                    answers.append(selected)
                    current_options = []

            elif line.upper().startswith('[X]') or line.startswith('[ ]'):
                current_options.append(line)

    if current_options:
        selected = _get_selected_option(current_options)
        answers.append(selected)

    if len(answers) != 100:
        raise ValueError(
            f"Expected 100 questions in '{file_path}', "
            f"but found {len(answers)}."
        )

    return answers


def _get_selected_option(options: list) -> int:
    """
    Determine which option was selected from a list of answer option lines.

    This is a private helper function used internally by
    extract_answers_sequence. It inspects each option line and returns
    the 1-indexed position of the line beginning with '[x]'.

    Parameters
    ----------
    options : list of str
        A list of up to 4 answer option strings, each starting with
        '[x]' (selected) or '[ ]' (not selected).

    Returns
    -------
    int
        The 1-indexed position (1-4) of the selected option,
        or 0 if no option was selected (unanswered question).
    """
    for i, option in enumerate(options, start=1):
        if option.lower().startswith('[x]'):
            return i
    return 0


def write_answers_sequence(answers: list, n: int, destination_path: str) -> None:
    """
    Write an extracted answer sequence to a text file.

    The output file is named 'answers_list_respondent_n.txt' and is saved
    inside the folder specified by destination_path. Each answer integer
    is written on a separate line.

    Parameters
    ----------
    answers : list of int
        A list of exactly 100 integers representing the answer sequence,
        where each value is 1, 2, 3, 4, or 0 (unanswered).
    n : int
        The respondent's identifier (positive integer), used in the
        output filename.
    destination_path : str
        The folder path where the output file should be saved.
        The folder must already exist.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If answers does not contain exactly 100 entries.
    FileNotFoundError
        If destination_path does not exist.
    TypeError
        If n is not a positive integer.

    Examples
    --------
    >>> write_answers_sequence(answers, 1, 'output')
    # Creates 'output/answers_list_respondent_1.txt'
    """
    if len(answers) != 100:
        raise ValueError(
            f"Expected a list of 100 answers, but got {len(answers)}."
        )

    if not isinstance(n, int) or n <= 0:
        raise TypeError(
            f"Respondent ID 'n' must be a positive integer, got: {n}"
        )

    if not os.path.isdir(destination_path):
        raise FileNotFoundError(
            f"Destination folder does not exist: {destination_path}"
        )

    filename = f"answers_list_respondent_{n}.txt"
    output_file = os.path.join(destination_path, filename)

    with open(output_file, 'w', encoding='utf-8') as f:
        for answer in answers:
            f.write(f"{answer}\n")

    print(f"[M1] Written: {output_file}")
