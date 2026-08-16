"""
main.py
=======
Entry point for the Student Management System.

HOW TO RUN
----------
1. Normal run (Loguru + PySnooper active):
       python main.py

2. Profile with cProfile, then visualize with SnakeViz:
       python -m cProfile -o result.profile main.py
       snakeviz result.profile

3. Trace execution with VizTracer:
       viztracer -o result.html --open main.py

TOOL SUMMARY
------------
  Loguru     → student_system.log + coloured console (all modules)
  PySnooper  → pysnooper_trace.log (student_service.py functions)
  cProfile   → run via terminal, visualised with SnakeViz
  VizTracer  → run via terminal, produces interactive result.html
"""

import sys
import os
import platform

# ── Make sure sibling packages are importable when run from any cwd ──────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Boot logging FIRST (before any other import logs anything) ───────────────
from utils.logger_setup import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

# ── Now import the rest ──────────────────────────────────────────────────────
from services.student_service import (
    list_students, add_student, search_student,
    remove_student, update_student, sort_by_name, sort_by_grade, export_to_csv,sort_by_major,
)
from services.report_service import print_full_report
from utils.validators import validate_menu_choice


# ── Display helpers ───────────────────────────────────────────────────────────

def _print_menu() -> None:
    print("""
  ╔══════════════════════════════════════════════════════╗
  ║        Welcome To Student Management System          ║
  ╠══════════════════════════════════════════════════════╣
  ║  1. View all students                                ║
  ║  2. Add a new student                                ║
  ║  3. Search for a student                             ║
  ║  4. Remove a student                                 ║
  ║  5. Update a student                                 ║
  ║  6. Full report (stats + classification)             ║
  ║  7. Sort students                                    ║
  ║  8. Export to CSV                                    ║
  ║  0. Exit                                             ║
  ╚══════════════════════════════════════════════════════╝""")


def _print_students(students, page_size: int = 10) -> None:
    if not students:
        print("  (no students to display)")
        return
    total = len(students)
    for start in range(0, total, page_size):
        page = students[start:start + page_size]
        print()
        for s in page:
            print(f"  {s}")
        end = min(start + page_size, total)
        print(f"\n  Showing {start + 1}-{end} of {total}")
        if end < total:
            input("  Press Enter for next page...")
    print()


# ── Menu actions ──────────────────────────────────────────────────────────────

@logger.catch(level="ERROR", message="Error in view_students")
def action_view():
    logger.info("User selected: View all students.")
    print("\n  Sort by:\n  1. Name\n  2. GPA\n  3. Major\n  4. No sorting")
    raw = input("  Choice: ").strip()
    students = list_students()
    if raw == "1":
        students = sort_by_name(students)
    elif raw == "2":
        students = sort_by_grade(students)
    elif raw == "3":
        students = sort_by_major(students)
    print(f"\n  ── All Students ({len(students)}) ──")
    _print_students(students)


@logger.catch(level="ERROR", message="Error in add_student")
def action_add():
    logger.info("User selected: Add new student.")
    print("\n  ── Add New Student ──")
    name       = input("  Name        : ").strip()
    student_id = input("  Student ID  : ").strip()
    grade      = input("  GPA (0-4.0) : ").strip()
    major      = input("  Major       : ").strip()
    try:
        student = add_student(name, student_id, grade, major)
        print(f"\n  ✓ Added: {student}\n")
    except ValueError as e:
        logger.warning(f"Add failed: {e}")
        print(f"\n  ✗ Error: {e}\n")


@logger.catch(level="ERROR", message="Error in search_student")
def action_search():
    logger.info("User selected: Search student.")
    query = input("\n  Enter name or ID to search: ").strip()
    results = search_student(query)
    print(f"\n  ── Search results for '{query}' ({len(results)} found) ──")
    _print_students(results)


@logger.catch(level="ERROR", message="Error in remove_student")
def action_remove():
    logger.info("User selected: Remove student.")
    student_id = input("\n  Enter Student ID to remove: ").strip()
    try:
        removed = remove_student(student_id)
        print(f"\n  ✓ Removed: {removed}\n")
    except ValueError as e:
        logger.warning(f"Remove failed: {e}")
        print(f"\n  ✗ Error: {e}\n")


@logger.catch(level="ERROR", message="Error in update_student")
def action_update():
    logger.info("User selected: Update student.")
    print("\n  ── Update Student (leave blank to keep current value) ──")
    student_id = input("  Student ID to update : ").strip()
    name  = input("  New name (or Enter)  : ").strip() or None
    grade = input("  New GPA  (or Enter)  : ").strip() or None
    major = input("  New major (or Enter) : ").strip() or None
    try:
        updated = update_student(student_id, name=name, grade=grade, major=major)
        print(f"\n  ✓ Updated: {updated}\n")
    except ValueError as e:
        logger.warning(f"Update failed: {e}")
        print(f"\n  ✗ Error: {e}\n")


@logger.catch(level="ERROR", message="Error in sort_students")
def action_sort():
    logger.info("User selected: Sort students.")
    print("\n  Sort by:\n  1. Name (A→Z)\n  2. Name (Z→A)\n  3. GPA (High→Low)\n  4. GPA (Low→High)")
    raw = input("  Choice: ").strip()
    try:
        choice = validate_menu_choice(raw, 1, 4)
    except ValueError as e:
        print(f"\n  ✗ {e}\n")
        return
    students = list_students()
    if choice == 1:
        result = sort_by_name(students, reverse=False)
    elif choice == 2:
        result = sort_by_name(students, reverse=True)
    elif choice == 3:
        result = sort_by_grade(students, reverse=True)
    else:
        result = sort_by_grade(students, reverse=False)
    _print_students(result)

@logger.catch(level="ERROR", message="Error in export_csv")
def action_export_csv():
    logger.info("User selected: Export to CSV.")
    export_to_csv()
    print("\n  ✓ Students exported to students_export.csv\n")


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    logger.info("Program started.")
    ACTIONS = {
        1: action_view,
        2: action_add,
        3: action_search,
        4: action_remove,
        5: action_update,
        6: print_full_report,
        7: action_sort,
        8: action_export_csv,
    }

    while True:
        _print_menu()
        raw = input("  Select option: ").strip()
        try:
            choice = validate_menu_choice(raw, 0, 8)
        except ValueError as e:
            print(f"\n  ✗ {e}\n")
            logger.warning(f"Invalid menu input: '{raw}'")
            continue

        if choice == 0:
            logger.info("User exited the program.")
            x = "#" * 40
            print(f"\n{x}")
            print("#    Goodbye! Thank you for using SMS.   #")
            print(f"{x}\n")
            sys.exit(0)

        logger.debug(f"Menu choice: {choice}")
        ACTIONS[choice]()

        # Clear screen before next menu (like original project)
        input("  Press Enter to continue...")
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")


if __name__ == "__main__":
    main()


# # clean
# import sys
# import os
# import platform

# sys.path.insert(0, os.path.dirname(__file__))

# from services.student_service import (
#     list_students, add_student, search_student,
#     remove_student, update_student, sort_by_name, sort_by_grade,
# )
# from services.report_service import print_full_report
# from utils.validators import validate_menu_choice

# def _print_menu() -> None:
#     print("""
#   ╔══════════════════════════════════════════════════════╗
#   ║        Welcome To Student Management System          ║
#   ╠══════════════════════════════════════════════════════╣
#   ║  1. View all students                                ║
#   ║  2. Add a new student                                ║
#   ║  3. Search for a student                             ║
#   ║  4. Remove a student                                 ║
#   ║  5. Update a student                                 ║
#   ║  6. Full report (stats + classification)             ║
#   ║  7. Sort students                                    ║
#   ║  0. Exit                                             ║
#   ╚══════════════════════════════════════════════════════╝""")

# def _print_students(students):
#     if not students:
#         print("  (no students to display)")
#         return
#     print()
#     for s in students:
#         print(f"  {s}")
#     print()

# def action_view():
#     students = list_students()
#     print(f"\n  ── All Students ({len(students)}) ──")
#     _print_students(students)

# def action_add():
#     print("\n  ── Add New Student ──")
#     name       = input("  Name        : ").strip()
#     student_id = input("  Student ID  : ").strip()
#     grade      = input("  GPA (0-4.0) : ").strip()
#     major      = input("  Major       : ").strip()
#     try:
#         student = add_student(name, student_id, grade, major)
#         print(f"\n  ✓ Added: {student}\n")
#     except ValueError as e:
#         print(f"\n  ✗ Error: {e}\n")

# def action_search():
#     query = input("\n  Enter name or ID to search: ").strip()
#     results = search_student(query)
#     print(f"\n  ── Search results for '{query}' ({len(results)} found) ──")
#     _print_students(results)

# def action_remove():
#     student_id = input("\n  Enter Student ID to remove: ").strip()
#     try:
#         removed = remove_student(student_id)
#         print(f"\n  ✓ Removed: {removed}\n")
#     except ValueError as e:
#         print(f"\n  ✗ Error: {e}\n")

# def action_update():
#     print("\n  ── Update Student (leave blank to keep current value) ──")
#     student_id = input("  Student ID to update : ").strip()
#     name  = input("  New name (or Enter)  : ").strip() or None
#     grade = input("  New GPA  (or Enter)  : ").strip() or None
#     major = input("  New major (or Enter) : ").strip() or None
#     try:
#         updated = update_student(student_id, name=name, grade=grade, major=major)
#         print(f"\n  ✓ Updated: {updated}\n")
#     except ValueError as e:
#         print(f"\n  ✗ Error: {e}\n")

# def action_sort():
#     print("\n  Sort by:\n  1. Name (A→Z)\n  2. Name (Z→A)\n  3. GPA (High→Low)\n  4. GPA (Low→High)")
#     raw = input("  Choice: ").strip()
#     try:
#         choice = validate_menu_choice(raw, 1, 4)
#     except ValueError as e:
#         print(f"\n  ✗ {e}\n")
#         return
#     students = list_students()
#     if choice == 1:
#         result = sort_by_name(students, reverse=False)
#     elif choice == 2:
#         result = sort_by_name(students, reverse=True)
#     elif choice == 3:
#         result = sort_by_grade(students, reverse=True)
#     else:
#         result = sort_by_grade(students, reverse=False)
#     _print_students(result)

# def main():
#     actions = {
#         1: action_view,
#         2: action_add,
#         3: action_search,
#         4: action_remove,
#         5: action_update,
#         6: print_full_report,
#         7: action_sort,
#     }

#     while True:
#         _print_menu()
#         raw = input("  Select option: ").strip()
#         try:
#             choice = validate_menu_choice(raw, 0, 7)
#         except ValueError as e:
#             print(f"\n  ✗ {e}\n")
#             continue

#         if choice == 0:
#             x = "#" * 40
#             print(f"\n{x}")
#             print("#    Goodbye! Thank you for using SMS.   #")
#             print(f"{x}\n")
#             sys.exit(0)

#         actions[choice]()

#         input("  Press Enter to continue...")
#         if platform.system() == "Windows":
#             os.system("cls")
#         else:
#             os.system("clear")

# if __name__ == "__main__":
#     main()