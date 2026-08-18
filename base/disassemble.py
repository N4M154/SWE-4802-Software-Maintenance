# import dis
# from utils import validators

# dis.dis(validators)

import dis
import io
from utils.logger_setup import get_logger

logger = get_logger(__name__)

# Paste the ORIGINAL (pre-fix) validate_grade here — no None guard yet
def validate_grade(grade_str: str) -> float:
    """
    Validate a GPA value.
    Must be a number in the range 0.0 – 4.0.
    """
    try:
        grade = float(grade_str.strip())
    except ValueError:
        logger.warning(f"Non-numeric grade entered: '{grade_str}'")
        raise ValueError("Grade must be a numeric value.")
    if not (0.0 <= grade <= 4.0):
        logger.warning(f"Grade out of range: {grade}")
        raise ValueError("Grade (GPA) must be between 0.0 and 4.0.")
    return round(grade, 2)

buffer = io.StringIO()
dis.dis(validate_grade, file=buffer)

with open("validate_grade_disassembly.txt", "w") as f:
    f.write(buffer.getvalue())

print("Done — check validate_grade_disassembly.txt")