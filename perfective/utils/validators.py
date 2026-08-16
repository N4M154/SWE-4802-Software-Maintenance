"""
utils/validators.py
===================
Input validation helpers.
All functions raise ValueError on bad input so callers can handle cleanly.
"""

import re
from utils.logger_setup import get_logger

logger = get_logger(__name__)


def validate_name(name: str) -> str:
    """
    Validate and normalise a student name.
    - Must be 2–60 characters
    - Only letters, spaces, hyphens, apostrophes
    Returns the title-cased name.
    """
    name = name.strip()
    if len(name) < 2 or len(name) > 60:
        logger.warning(f"Name length out of range: '{name}'")
        raise ValueError("Name must be between 2 and 60 characters.")
    if not re.fullmatch(r"[A-Za-z\s\-']+", name):
        logger.warning(f"Name contains invalid characters: '{name}'")
        raise ValueError("Name may only contain letters, spaces, hyphens, or apostrophes.")
    return name.title()


def validate_student_id(student_id: str) -> str:
    """
    Validate a student ID.
    Expected format: letters + digits, e.g. STU001 or S12345 (3–10 chars).
    """
    student_id = student_id.strip().upper()
    if not re.fullmatch(r"[A-Z]{1,4}\d{2,8}", student_id):
        logger.warning(f"Invalid student ID format: '{student_id}'")
        raise ValueError(
            "Student ID must start with 1-4 letters followed by 2-8 digits (e.g. STU001)."
        )
    return student_id


def validate_grade(grade_str: str) -> float:
    """
    Validate a GPA value.
    Must be a number in the range 0.0 – 4.0.
    """
    if grade_str is None:
        logger.warning("Grade value was None.")
        raise ValueError("Grade must be a numeric value.")
    try:
        grade = float(grade_str.strip())
    except ValueError:
        logger.warning(f"Non-numeric grade entered: '{grade_str}'")
        raise ValueError("Grade must be a numeric value.")
    if not (0.0 <= grade <= 4.0):
        logger.warning(f"Grade out of range: {grade}")
        raise ValueError("Grade (GPA) must be between 0.0 and 4.0.")
    return round(grade, 2)


def validate_major(major: str) -> str:
    """
    Validate a major/field-of-study string.
    Must be 2–80 printable characters.
    """
    major = major.strip()
    if len(major) < 2 or len(major) > 80:
        logger.warning(f"Major length out of range: '{major}'")
        raise ValueError("Major must be between 2 and 80 characters.")
    return major.title()


def validate_menu_choice(raw: str, low: int, high: int) -> int:
    """
    Parse and validate a menu option integer in [low, high].
    """
    try:
        choice = int(raw.strip())
    except ValueError:
        raise ValueError("Please enter a whole number.")
    if not (low <= choice <= high):
        raise ValueError(f"Please enter a number between {low} and {high}.")
    return choice



# # without the logger codes
# import re

# def validate_name(name: str) -> str:
#     """
#     Validate and normalise a student name.
#     - Must be 2–60 characters
#     - Only letters, spaces, hyphens, apostrophes
#     Returns the title-cased name.
#     """
#     name = name.strip()
#     if len(name) < 2 or len(name) > 60:
#         raise ValueError("Name must be between 2 and 60 characters.")
#     if not re.fullmatch(r"[A-Za-z\s\-']+", name):
#         raise ValueError("Name may only contain letters, spaces, hyphens, or apostrophes.")
#     return name.title()

# def validate_student_id(student_id: str) -> str:
#     """
#     Validate a student ID.
#     Expected format: letters + digits, e.g. STU001 or S12345 (3–10 chars).
#     """
#     student_id = student_id.strip().upper()
#     if not re.fullmatch(r"[A-Z]{1,4}\d{2,8}", student_id):
#         raise ValueError(
#             "Student ID must start with 1-4 letters followed by 2-8 digits (e.g. STU001)."
#         )
#     return student_id

# def validate_grade(grade_str: str) -> float:
#     """
#     Validate a GPA value.
#     Must be a number in the range 0.0 – 4.0.
#     """
#     try:
#         grade = float(grade_str.strip())
#     except ValueError:
#         raise ValueError("Grade must be a numeric value.")
#     if not (0.0 <= grade <= 4.0):
#         raise ValueError("Grade (GPA) must be between 0.0 and 4.0.")
#     return round(grade, 2)

# def validate_major(major: str) -> str:
#     """
#     Validate a major/field-of-study string.
#     Must be 2–80 printable characters.
#     """
#     major = major.strip()
#     if len(major) < 2 or len(major) > 80:
#         raise ValueError("Major must be between 2 and 80 characters.")
#     return major.title()

# def validate_menu_choice(raw: str, low: int, high: int) -> int:
#     """
#     Parse and validate a menu option integer in [low, high].
#     """
#     try:
#         choice = int(raw.strip())
#     except ValueError:
#         raise ValueError("Please enter a whole number.")
#     if not (low <= choice <= high):
#         raise ValueError(f"Please enter a number between {low} and {high}.")
#     return choice