## Unreleased

### Fixed

- `validate_grade()` now raises a clean `ValueError` instead of crashing with `AttributeError` when passed `None`.

### Added

- CSV export capability via a new `export_to_csv()` function and
  menu option 8, for integration with external reporting systems.
  \end{lstlisting}
- Basic regression test suite for `utils/validators.py`.

### Changed

- Extracted GPA classification thresholds in `Student.classification()`
  into named module-level constants.
