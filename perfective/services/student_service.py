"""
services/student_service.py
============================
CRUD operations and sorting for the student list.
PySnooper is applied to every mutating function so variable
changes are traced to pysnooper_trace.log.
"""

import csv
import json
import os
import pysnooper
from typing import List, Optional

from models.student import Student
from utils.logger_setup import get_logger
from utils.validators import validate_name, validate_student_id, validate_grade, validate_major

logger = get_logger(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "students.json")


# ── Persistence helpers ───────────────────────────────────────────────────────

def _load_data() -> List[Student]:
    """Read students from JSON file. Returns empty list if file missing."""
    path = os.path.abspath(DATA_FILE)
    if not os.path.exists(path):
        logger.debug(f"Data file not found at {path}; starting with empty list.")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            records = json.load(f)
        students = [Student.from_dict(r) for r in records]
        logger.debug(f"Loaded {len(students)} student(s) from {path}.")
        return students
    except (json.JSONDecodeError, KeyError) as exc:
        logger.error(f"Failed to parse data file: {exc}")
        return []


def _save_data(students: List[Student]) -> None:
    """Write current student list back to JSON file."""
    path = os.path.abspath(DATA_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in students], f, indent=2)
    logger.debug(f"Saved {len(students)} student(s) to {path}.")

def export_to_csv(path: str = "students_export.csv") -> None:
    """
    Export all students to a CSV file for external systems
    that require CSV rather than JSON.
    """
    students = _load_data()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "student_id", "grade",
                        "major", "enrolled", "created_at"]
        )
        writer.writeheader()
        for s in students:
            writer.writerow(s.to_dict())
    logger.success(f"Exported {len(students)} student(s) to {path}.")


# ── CRUD operations ───────────────────────────────────────────────────────────

@pysnooper.snoop("pysnooper_trace.log")
def list_students(enrolled_only: bool = False) -> List[Student]:
    """
    Return all students (or only enrolled ones).
    PySnooper traces the filtering loop.
    """
    logger.info(f"Listing students (enrolled_only={enrolled_only}).")
    students = _load_data()
    if enrolled_only:
        students = [s for s in students if s.enrolled]
    logger.debug(f"Returning {len(students)} student(s).")
    return students


@pysnooper.snoop("pysnooper_trace.log")
def add_student(name: str, student_id: str, grade: str, major: str) -> Student:
    """
    Validate inputs, create a Student, append to storage.
    PySnooper traces every variable change.
    """
    logger.info(f"Attempting to add student: name='{name}', id='{student_id}'.")

    # Validate
    name       = validate_name(name)
    student_id = validate_student_id(student_id)
    grade_val  = validate_grade(grade)
    major      = validate_major(major)

    students = _load_data()

    # Duplicate ID check
    existing_ids = [s.student_id for s in students]
    if student_id in existing_ids:
        logger.warning(f"Duplicate student ID: '{student_id}'.")
        raise ValueError(f"A student with ID '{student_id}' already exists.")

    new_student = Student(name=name, student_id=student_id, grade=grade_val, major=major)
    students.append(new_student)
    _save_data(students)

    logger.success(f"Added: {new_student}")
    return new_student


@pysnooper.snoop("pysnooper_trace.log")
def search_student(query: str) -> List[Student]:
    """
    Case-insensitive search by name or student ID.
    PySnooper traces the match loop.
    """
    logger.info(f"Searching for: '{query}'.")
    query = query.strip().lower()
    students = _load_data()
    results = [
        s for s in students
        if query in s.name.lower() or query in s.student_id.lower()
    ]
    logger.debug(f"Search returned {len(results)} result(s) for '{query}'.")
    return results


@pysnooper.snoop("pysnooper_trace.log")
def remove_student(student_id: str) -> Student:
    """
    Remove a student by ID. Raises ValueError if not found.
    PySnooper traces the removal.
    """
    logger.info(f"Attempting to remove student ID: '{student_id}'.")
    student_id = student_id.strip().upper()
    students = _load_data()

    target: Optional[Student] = None
    for s in students:
        if s.student_id == student_id:
            target = s
            break

    if target is None:
        logger.error(f"Student ID '{student_id}' not found.")
        raise ValueError(f"No student found with ID '{student_id}'.")

    students.remove(target)
    _save_data(students)
    logger.success(f"Removed: {target}")
    return target


@pysnooper.snoop("pysnooper_trace.log")
def update_student(student_id: str, name: str = None, grade: str = None, major: str = None) -> Student:
    """
    Update one or more fields of an existing student.
    PySnooper traces every field change.
    """
    logger.info(f"Attempting to update student ID: '{student_id}'.")
    student_id = student_id.strip().upper()
    students = _load_data()

    target: Optional[Student] = None
    for s in students:
        if s.student_id == student_id:
            target = s
            break

    if target is None:
        logger.error(f"Student ID '{student_id}' not found for update.")
        raise ValueError(f"No student found with ID '{student_id}'.")

    if name is not None:
        target.name = validate_name(name)
        logger.debug(f"Updated name to '{target.name}'.")
    if grade is not None:
        target.grade = validate_grade(grade)
        logger.debug(f"Updated grade to {target.grade}.")
    if major is not None:
        target.major = validate_major(major)
        logger.debug(f"Updated major to '{target.major}'.")

    _save_data(students)
    logger.success(f"Updated: {target}")
    return target


# ── Sorting helpers ───────────────────────────────────────────────────────────

def sort_by_name(students: List[Student], reverse: bool = False) -> List[Student]:
    logger.debug(f"Sorting {len(students)} student(s) by name (reverse={reverse}).")
    return sorted(students, key=lambda s: s.name.lower(), reverse=reverse)


def sort_by_grade(students: List[Student], reverse: bool = True) -> List[Student]:
    logger.debug(f"Sorting {len(students)} student(s) by grade (reverse={reverse}).")
    return sorted(students, key=lambda s: s.grade, reverse=reverse)

def sort_by_major(students: List[Student], reverse: bool = False) -> List[Student]:
    logger.debug(f"Sorting {len(students)} student(s) by major (reverse={reverse}).")
    return sorted(students, key=lambda s: s.major.lower(), reverse=reverse)


# # without any PySnooper, Loguru codes

# import json
# import os
# from typing import List, Optional

# from models.student import Student
# from utils.validators import validate_name, validate_student_id, validate_grade, validate_major

# DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "students.json")

# # ── Persistence helpers ───────────────────────────────────────────────────────

# def _load_data() -> List[Student]:
#     """Read students from JSON file. Returns empty list if file missing."""
#     path = os.path.abspath(DATA_FILE)
#     if not os.path.exists(path):
#         return []
#     try:
#         with open(path, "r", encoding="utf-8") as f:
#             records = json.load(f)
#         return [Student.from_dict(r) for r in records]
#     except (json.JSONDecodeError, KeyError):
#         return []

# def _save_data(students: List[Student]) -> None:
#     """Write current student list back to JSON file."""
#     path = os.path.abspath(DATA_FILE)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump([s.to_dict() for s in students], f, indent=2)

# # ── CRUD operations ───────────────────────────────────────────────────────────

# def list_students(enrolled_only: bool = False) -> List[Student]:
#     """Return all students (or only enrolled ones)."""
#     students = _load_data()
#     if enrolled_only:
#         students = [s for s in students if s.enrolled]
#     return students

# def add_student(name: str, student_id: str, grade: str, major: str) -> Student:
#     """Validate inputs, create a Student, append to storage."""
#     # Validate
#     name       = validate_name(name)
#     student_id = validate_student_id(student_id)
#     grade_val  = validate_grade(grade)
#     major      = validate_major(major)

#     students = _load_data()

#     # Duplicate ID check
#     existing_ids = [s.student_id for s in students]
#     if student_id in existing_ids:
#         raise ValueError(f"A student with ID '{student_id}' already exists.")

#     new_student = Student(name=name, student_id=student_id, grade=grade_val, major=major)
#     students.append(new_student)
#     _save_data(students)
#     return new_student

# def search_student(query: str) -> List[Student]:
#     """Case-insensitive search by name or student ID."""
#     query = query.strip().lower()
#     students = _load_data()
#     results = [
#         s for s in students
#         if query in s.name.lower() or query in s.student_id.lower()
#     ]
#     return results

# def remove_student(student_id: str) -> Student:
#     """Remove a student by ID. Raises ValueError if not found."""
#     student_id = student_id.strip().upper()
#     students = _load_data()

#     target: Optional[Student] = None
#     for s in students:
#         if s.student_id == student_id:
#             target = s
#             break

#     if target is None:
#         raise ValueError(f"No student found with ID '{student_id}'.")

#     students.remove(target)
#     _save_data(students)
#     return target

# def update_student(student_id: str, name: str = None, grade: str = None, major: str = None) -> Student:
#     """Update one or more fields of an existing student."""
#     student_id = student_id.strip().upper()
#     students = _load_data()

#     target: Optional[Student] = None
#     for s in students:
#         if s.student_id == student_id:
#             target = s
#             break

#     if target is None:
#         raise ValueError(f"No student found with ID '{student_id}'.")

#     if name is not None:
#         target.name = validate_name(name)
#     if grade is not None:
#         target.grade = validate_grade(grade)
#     if major is not None:
#         target.major = validate_major(major)

#     _save_data(students)
#     return target

# # ── Sorting helpers ───────────────────────────────────────────────────────────

# def sort_by_name(students: List[Student], reverse: bool = False) -> List[Student]:
#     return sorted(students, key=lambda s: s.name.lower(), reverse=reverse)

# def sort_by_grade(students: List[Student], reverse: bool = True) -> List[Student]:
#     return sorted(students, key=lambda s: s.grade, reverse=reverse)