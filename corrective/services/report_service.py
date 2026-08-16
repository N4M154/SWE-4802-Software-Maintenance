"""
services/report_service.py
===========================
Statistics, classification summaries, and formatted reports.
Uses cProfile-friendly plain functions (no decorators that add overhead).
VizTracer will capture all calls automatically when run via:
    viztracer -o result.html --open main.py
"""

from typing import List, Dict
from models.student import Student
from services.student_service import list_students, sort_by_grade
from utils.logger_setup import get_logger

logger = get_logger(__name__)


def compute_stats(students: List[Student]) -> Dict:
    """
    Compute summary statistics for a list of students.
    Returns a dict with count, average GPA, highest, lowest.
    """
    logger.info(f"Computing stats for {len(students)} student(s).")

    if not students:
        logger.warning("No students provided for stats computation.")
        return {
            "count":   0,
            "average": 0.0,
            "highest": None,
            "lowest":  None,
        }

    grades = [s.grade for s in students]
    stats = {
        "count":   len(students),
        "average": round(sum(grades) / len(grades), 2),
        "highest": max(grades),
        "lowest":  min(grades),
    }
    logger.debug(f"Stats: {stats}")
    return stats


def classify_students(students: List[Student]) -> Dict[str, List[Student]]:
    """
    Group students into academic standing buckets:
      Distinction (≥3.7), Merit (≥3.0), Pass (≥2.0), At Risk (<2.0)
    """
    logger.info("Classifying students by academic standing.")
    buckets: Dict[str, List[Student]] = {
        "Distinction": [],
        "Merit":       [],
        "Pass":        [],
        "At Risk":     [],
    }
    for student in students:
        bucket = student.classification()
        buckets[bucket].append(student)
        logger.debug(f"  {student.student_id} → {bucket}")
    return buckets


def major_breakdown(students: List[Student]) -> Dict[str, int]:
    """Return a count of students per major, sorted descending."""
    logger.info("Computing major breakdown.")
    counts: Dict[str, int] = {}
    for s in students:
        counts[s.major] = counts.get(s.major, 0) + 1
    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    logger.debug(f"Major breakdown: {sorted_counts}")
    return sorted_counts


def print_full_report() -> None:
    """
    Print a formatted full report to stdout.
    Loads fresh data, computes all metrics.
    Called from main menu option 6.
    """
    logger.info("Generating full report.")
    students = list_students()

    print("\n" + "=" * 56)
    print("          STUDENT MANAGEMENT SYSTEM — REPORT")
    print("=" * 56)

    # ── Overall stats ──────────────────────────────────────────
    stats = compute_stats(students)
    print(f"\n  Total students : {stats['count']}")
    print(f"  Average GPA    : {stats['average']:.2f}")
    print(f"  Highest GPA    : {stats['highest']}")
    print(f"  Lowest GPA     : {stats['lowest']}")

    # ── Classification ─────────────────────────────────────────
    print("\n  ── Academic Standing ──────────────────────────────")
    buckets = classify_students(students)
    for standing, group in buckets.items():
        ids = ", ".join(s.student_id for s in group) if group else "—"
        print(f"  {standing:<12} ({len(group):>2} students): {ids}")

    # ── Top 5 by GPA ───────────────────────────────────────────
    print("\n  ── Top 5 Students by GPA ──────────────────────────")
    top5 = sort_by_grade(students)[:5]
    if top5:
        for rank, s in enumerate(top5, 1):
            print(f"  {rank}. {s.name:<25} GPA: {s.grade:.2f}  [{s.student_id}]")
    else:
        print("  No students on record.")

    # ── Major breakdown ────────────────────────────────────────
    print("\n  ── Students per Major ─────────────────────────────")
    breakdown = major_breakdown(students)
    if breakdown:
        for major, count in breakdown.items():
            bar = "█" * count
            print(f"  {major:<30} {bar} ({count})")
    else:
        print("  No data.")

    print("\n" + "=" * 56 + "\n")
    logger.success("Full report printed.")




# # no logging
# from typing import List, Dict
# from models.student import Student
# from services.student_service import list_students, sort_by_grade

# def compute_stats(students: List[Student]) -> Dict:
#     """Compute summary statistics for a list of students."""
#     if not students:
#         return {
#             "count":   0,
#             "average": 0.0,
#             "highest": None,
#             "lowest":  None,
#         }
#     grades = [s.grade for s in students]
#     return {
#         "count":   len(students),
#         "average": round(sum(grades) / len(grades), 2),
#         "highest": max(grades),
#         "lowest":  min(grades),
#     }

# def classify_students(students: List[Student]) -> Dict[str, List[Student]]:
#     """Group students into academic standing buckets."""
#     buckets: Dict[str, List[Student]] = {
#         "Distinction": [],
#         "Merit":       [],
#         "Pass":        [],
#         "At Risk":     [],
#     }
#     for student in students:
#         bucket = student.classification()
#         buckets[bucket].append(student)
#     return buckets

# def major_breakdown(students: List[Student]) -> Dict[str, int]:
#     """Return a count of students per major, sorted descending."""
#     counts: Dict[str, int] = {}
#     for s in students:
#         counts[s.major] = counts.get(s.major, 0) + 1
#     return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

# def print_full_report() -> None:
#     """Print a formatted full report to stdout."""
#     students = list_students()

#     print("\n" + "=" * 56)
#     print("          STUDENT MANAGEMENT SYSTEM — REPORT")
#     print("=" * 56)

#     stats = compute_stats(students)
#     print(f"\n  Total students : {stats['count']}")
#     print(f"  Average GPA    : {stats['average']:.2f}")
#     print(f"  Highest GPA    : {stats['highest']}")
#     print(f"  Lowest GPA     : {stats['lowest']}")

#     print("\n  ── Academic Standing ──────────────────────────────")
#     buckets = classify_students(students)
#     for standing, group in buckets.items():
#         ids = ", ".join(s.student_id for s in group) if group else "—"
#         print(f"  {standing:<12} ({len(group):>2} students): {ids}")

#     print("\n  ── Top 5 Students by GPA ──────────────────────────")
#     top5 = sort_by_grade(students)[:5]
#     if top5:
#         for rank, s in enumerate(top5, 1):
#             print(f"  {rank}. {s.name:<25} GPA: {s.grade:.2f}  [{s.student_id}]")
#     else:
#         print("  No students on record.")

#     print("\n  ── Students per Major ─────────────────────────────")
#     breakdown = major_breakdown(students)
#     if breakdown:
#         for major, count in breakdown.items():
#             bar = "█" * count
#             print(f"  {major:<30} {bar} ({count})")
#     else:
#         print("  No data.")

#     print("\n" + "=" * 56 + "\n")