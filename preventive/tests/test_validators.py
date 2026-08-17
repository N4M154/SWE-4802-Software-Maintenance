import unittest
from utils.validators import (
    validate_name, validate_student_id,
    validate_grade, validate_major,
)


class TestValidators(unittest.TestCase):

    def test_validate_name_valid(self):
        self.assertEqual(validate_name("Yugesh Kumar"), "Yugesh Kumar")

    def test_validate_name_too_short(self):
        with self.assertRaises(ValueError):
            validate_name("A")

    def test_validate_student_id_valid(self):
        self.assertEqual(validate_student_id("stu001"), "STU001")

    def test_validate_student_id_invalid_format(self):
        with self.assertRaises(ValueError):
            validate_student_id("12345")

    def test_validate_grade_valid(self):
        self.assertEqual(validate_grade("3.5"), 3.5)

    def test_validate_grade_out_of_range(self):
        with self.assertRaises(ValueError):
            validate_grade("4.5")

    def test_validate_grade_non_numeric(self):
        with self.assertRaises(ValueError):
            validate_grade("abc")

    def test_validate_major_valid(self):
        self.assertEqual(validate_major("computer science"),
                          "Computer Science")


if __name__ == "__main__":
    unittest.main()