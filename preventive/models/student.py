"""
models/student.py
=================
Defines the Student data class used throughout the system.
"""

from dataclasses import dataclass, field
from datetime import datetime

DISTINCTION_THRESHOLD = 3.7
MERIT_THRESHOLD = 3.0
PASS_THRESHOLD = 2.0

@dataclass
class Student:
    """Represents a single student record."""
    name: str
    student_id: str
    grade: float          # GPA, 0.0 – 4.0
    major: str
    enrolled: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # ── Derived helpers ──────────────────────────────────────────────────────
    def classification(self) -> str:
        """Return academic standing based on GPA."""
        if self.grade >= DISTINCTION_THRESHOLD:
            return "Distinction"
        elif self.grade >= MERIT_THRESHOLD:
            return "Merit"
        elif self.grade >= PASS_THRESHOLD:
            return "Pass"
        else:
            return "At Risk"

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

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """Deserialize from a plain dict (from JSON storage)."""
        return cls(
            name=data["name"],
            student_id=data["student_id"],
            grade=float(data["grade"]),
            major=data["major"],
            enrolled=bool(data.get("enrolled", True)),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )

    def __str__(self) -> str:
        status = "Active" if self.enrolled else "Inactive"
        return (
            f"[{self.student_id}] {self.name} | "
            f"Major: {self.major} | GPA: {self.grade:.2f} | "
            f"Status: {status} | Standing: {self.classification()}"
        )