# import dis
# from utils import validators

# dis.dis(validators)


import dis
import io

# Paste the ORIGINAL (pre-refactor) classification method here,
# with the raw threshold literals still inline
class Student:
    def __init__(self, grade):
        self.grade = grade

    def classification(self) -> str:
        """Return academic standing based on GPA."""
        if self.grade >= 3.7:
            return "Distinction"
        elif self.grade >= 3.0:
            return "Merit"
        elif self.grade >= 2.0:
            return "Pass"
        else:
            return "At Risk"

buffer = io.StringIO()
dis.dis(Student.classification, file=buffer)

with open("classification_disassembly.txt", "w") as f:
    f.write(buffer.getvalue())

print("Done — check classification_disassembly.txt")