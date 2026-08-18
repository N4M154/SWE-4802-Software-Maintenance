# import dis
# from utils import validators

# dis.dis(validators)

import dis
import io
from dataclasses import dataclass, field
from datetime import datetime

# Paste the existing to_dict() method here for isolated disassembly
@dataclass
class Student:
    name: str
    student_id: str
    grade: float
    major: str
    enrolled: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Serialize to plain dict (for JSON storage)."""
        return {
            "name":       self.name,
            "student_id": self.student_id,
            "grade":      self.grade,
            "major":      self.major,
            "enrolled":   self.enrolled,
            "created_at": self.created_at,
        }

buffer = io.StringIO()
dis.dis(Student.to_dict, file=buffer)

with open("to_dict_disassembly.txt", "w") as f:
    f.write(buffer.getvalue())

print("Done — check to_dict_disassembly.txt")