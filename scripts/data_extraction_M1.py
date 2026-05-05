"""
data_extraction_M1.py


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
 Extract the sequence of answers that a respondent selected from a text file that
 contains the raw data from each respondent.

 This function will read the file that contains the 100 questions with the answer
 choices denoted by brackets. When the function detects either [x] or [X] it will 
 record the selected answer for that question (answers are denoted as 1-4). If
 the brackets within the question remain empty [ ] the question will be recorded
 as a 0 indicating that the respondent did not answer that question.


 Parameters
 ----------

 file_path : str
     The relative or absolute path to the file containing the quiz answers from 
     each respondent.

 Returns
 -------

 list of int
     A list containing the sequence of 100 answers selected by the respondent.

 Raises
 ------
 FileNotFoundError
     FileNotFoundError will be raised if the text file cannot be located.
 ValueError
     ValueError will be raised if the document does not contain the 100 quiz
     questions that were defined in the quiz.

 Notes
 -----
 The function is case-insensitive in that it will detect both upper- and lowercase
 'X' answers from the respondents.

 Examples
 --------
 >> extract_answers_sequence('data/a1.txt')
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
  Determine which of the answer options was selected.
  This is a private helper function used internally by
  extract_answers_sequence. It inspects each option line to determine
  which line begins with '[x]'.

  Parameters
  ----------
  options : list of str
    A list of up to 4 answer option strings, each beginning with
    '[x]' (selected) or '[ ]' (not selected).

  Returns
  -------
  int
    The 1-indexed position (1-4) of the selected answer option,
    0 if no answer option was selected (unanswered question).
    """
    for i, option in enumerate(options, start=1):
        if option.lower().startswith('[x]'):
            return i
    return 0


def write_answers_sequence(answers: list, n: int, destination_path: str) -> None:
    """
Write an extracted answer sequence to a text file.
The output file is named according to the format 'answers_list_respondent_n.txt' and is
saved inside the folder specified by the argument 'destination_path'. Each answer
 integer is written on a separate line within the text file.

Parameters
----------
answers : list of int
  A list of 100 integers between 1 and 4 (or 0 for unanswered questions).
n : int
 The identifier of the respondent providing the answers.
destination_path : str
    The path of the folder in which the text file should be created and saved.

Returns
-------
None

Raises
------
ValueError
    If the 'answers' list does not contain 100 integers
FileNotFoundError
    If the 'destination_path' folder does not exist
TypeError
    If the 'n' argument is not of type 'int' or is less than or equal to 0.

Examples
--------
>> write_answers_sequence(answers, 1, 'output')
    
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
