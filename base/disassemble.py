# import dis
# from utils import validators

# dis.dis(validators)


import dis
import io

# Paste the ORIGINAL (pre-pagination) _print_students function here
# so it can be disassembled in isolation
def _print_students(students) -> None:
    if not students:
        print("  (no students to display)")
        return
    print()
    for s in students:
        print(f"  {s}")
    print()

buffer = io.StringIO()
dis.dis(_print_students, file=buffer)

with open("print_students_disassembly.txt", "w") as f:
    f.write(buffer.getvalue())

print("Done — check print_students_disassembly.txt")