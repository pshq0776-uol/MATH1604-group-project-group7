"""
data_analysis_M3.py
===================
Module for statistical analysis and visualisation of collated quiz responses.

Author: Danish Imran Agus
Student ID: 202023762
Role: Team Member 3
"""

import os
import re
import matplotlib.pyplot as plt


def _parse_collated_file(collated_answers_path: str) -> list:
    """
    Parse a collated answers file into a list of individual answer sequences.

    Splits the collated file on asterisk separators and extracts a list
    of integers (1-4 or 0) for each respondent.

    Parameters
    ----------
    collated_answers_path : str
        Path to the collated_answers.txt file.

    Returns
    -------
    list of list of int
        A list where each element is a list of 100 integers representing
        one respondent's answer sequence.

    Raises
    ------
    FileNotFoundError
        If collated_answers_path does not point to an existing file.
    """
    if not os.path.exists(collated_answers_path):
        raise FileNotFoundError(
            f"Collated answers file not found: '{collated_answers_path}'"
        )

    with open(collated_answers_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    raw_blocks = re.split(r'\n\*\n', full_text)
    all_sequences = []

    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
        answers = _extract_from_block(block)
        if answers:
            all_sequences.append(answers)

    return all_sequences


def _extract_from_block(block: str) -> list:
    """
    Extract a single respondent's answer sequence from a raw text block.

    Parameters
    ----------
    block : str
        A multi-line string containing one respondent's quiz answer text.

    Returns
    -------
    list of int
        A list of up to 100 integers (1-4 or 0). Returns an empty list
        if no valid question blocks are found.
    """
    answers = []
    current_options = []

    for line in block.splitlines():
        line = line.strip()

        if re.match(r'^Question\s+\d+\.', line):
            if current_options:
                answers.append(_get_selected(current_options))
                current_options = []

        elif line.startswith('[x]') or line.startswith('[ ]'):
            current_options.append(line)

    if current_options:
        answers.append(_get_selected(current_options))

    return answers if len(answers) == 100 else []


def _get_selected(options: list) -> int:
    """
    Return the 1-indexed position of the selected answer option.

    Parameters
    ----------
    options : list of str
        A list of answer lines, each starting with '[x]' or '[ ]'.

    Returns
    -------
    int
        Position (1-4) of the '[x]' line, or 0 if none is marked.
    """
    for i, opt in enumerate(options, start=1):
        if opt.startswith('[x]'):
            return i
    return 0


def generate_means_sequence(collated_answers_path: str) -> list:
    """
    Compute the mean answer value per question across all respondents.

    Reads the collated answers file, extracts all respondent sequences,
    and for each of the 100 questions calculates the arithmetic mean of
    the answers given. Unanswered questions (coded as 0) are excluded
    from the mean calculation for that question.

    Parameters
    ----------
    collated_answers_path : str
        Path to the collated_answers.txt file.

    Returns
    -------
    list of float
        A list of exactly 100 floats representing the mean answer
        per question.

    Raises
    ------
    FileNotFoundError
        If collated_answers_path does not point to an existing file.
    RuntimeError
        If no valid respondent sequences could be parsed from the file.

    Examples
    --------
    >>> means = generate_means_sequence('output/collated_answers.txt')
    >>> print(means[:5])
    [2.453, 1.031, 3.875, 2.0, 4.0]
    """
    all_sequences = _parse_collated_file(collated_answers_path)

    if not all_sequences:
        raise RuntimeError(
            "No valid respondent sequences found in the collated file."
        )

    means = []
    for q_idx in range(100):
        valid_answers = [
            seq[q_idx] for seq in all_sequences if seq[q_idx] != 0
        ]
        if valid_answers:
            means.append(sum(valid_answers) / len(valid_answers))
        else:
            means.append(0.0)

    print(f"[M3] Means computed over {len(all_sequences)} respondent(s).")
    return means


def visualize_data(collated_answers_path: str, n: int) -> None:
    """
    Visualise the quiz answer data as either a scatter plot or a line plot.

    Parameters
    ----------
    collated_answers_path : str
        Path to the collated_answers.txt file.
    n : int
        Plot type selector:
        - 1 for a scatter plot of means per question,
        - 2 for a line plot of all individual answer sequences.

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        If collated_answers_path does not point to an existing file.

    Examples
    --------
    >>> visualize_data('output/collated_answers.txt', 1)
    >>> visualize_data('output/collated_answers.txt', 2)
    >>> visualize_data('output/collated_answers.txt', 3)
    [M3] ERROR: Invalid plot type n=3.
    """
    if n not in (1, 2):
        print(
            f"[M3] ERROR: Invalid plot type n={n}. "
            "Please use n=1 (scatter plot) or n=2 (line plot)."
        )
        return

    all_sequences = _parse_collated_file(collated_answers_path)

    if not all_sequences:
        print("[M3] ERROR: No valid sequences found — cannot produce plot.")
        return

    questions = list(range(1, 101))

    if n == 1:
        means = generate_means_sequence(collated_answers_path)

        fig, ax = plt.subplots(figsize=(14, 5))
        ax.scatter(questions, means, color='steelblue', s=30, alpha=0.8,
                   label='Mean answer')
        ax.axhline(y=2.5, color='red', linestyle='--', linewidth=1,
                   label='Expected mean if random (2.5)')
        ax.set_title('Mean Answer Value per Question', fontsize=14)
        ax.set_xlabel('Question Number', fontsize=12)
        ax.set_ylabel('Mean Answer Value (1-4)', fontsize=12)
        ax.set_xlim(0.5, 100.5)
        ax.set_ylim(0.5, 4.5)
        ax.set_yticks([1, 2, 3, 4])
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        print("[M3] Scatter plot displayed.")

    elif n == 2:
        fig, ax = plt.subplots(figsize=(14, 6))
        for seq in all_sequences:
            ax.plot(questions, seq, linewidth=0.6, alpha=0.4, color='steelblue')
        ax.set_title(f'Answer Sequences for All {len(all_sequences)} Respondents',
                     fontsize=14)
        ax.set_xlabel('Question Number', fontsize=12)
        ax.set_ylabel('Answer Selected (1-4, 0=unanswered)', fontsize=12)
        ax.set_xlim(0.5, 100.5)
        ax.set_ylim(-0.1, 4.5)
        ax.set_yticks([0, 1, 2, 3, 4])
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        print(f"[M3] Line plot displayed ({len(all_sequences)} respondents).")
