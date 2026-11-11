# Lab 7: Fuzz Testing with Hypothesis

**Student Name:** Sujeet V Bire  
**SRN:** PES1UG24CS716  
**Department:** Computer Science and Engineering  
**Institution:** PES University  
**Course:** Software Engineering Lab — Semester VII  
**Assigned Repository:** `SETAPESU26/L6_L7_52_visa_application` (`Visa Application System`)  

---

## 1. Lab Title & Objective

**Lab 7 — Fuzz Testing for Input Validation Bugs**  
The objective of this laboratory assignment is to apply property-based fuzz testing using Python's **Hypothesis** framework to uncover and remediate latent input validation bugs, unhandled exceptions, perimeter parsing vulnerabilities, and arithmetic overflow errors in a visa application processing system.

---

## 2. Project Architecture & Single Source of Truth (SSOT)

- **Canonical Domain Implementation (`visa_application.py`):**  
  The primary single source of truth containing all domain validation logic, alphabetic token parsing, numerical day aggregation, financial tax calculations with 18% GST, and strict floating-point arithmetic overflow guards (`if not math.isfinite(raw_total): return None`).
- **Compatibility Wrapper (`processor.py`):**  
  An explicit wrapper module that imports and re-exports `parse_application`, `processing_average`, `payable_fee`, and the interactive `main()` CLI runner from `visa_application.py`, satisfying generic automated grading requirements without duplicating code.
- **Canonical Test Suite (`test_visa_application.py`):**  
  11 Hypothesis property-based fuzz tests directly exercising `visa_application.py`.
- **Compatibility Test Suite (`test_processor.py`):**  
  11 Hypothesis property-based fuzz tests verifying the compatibility wrapper `processor.py`.
- **Formal PDF Report (`Lab_7_FuzzTesting_Report.pdf`):**  
  Comprehensive 8-page, 17-section academic lab report containing architecture diagrams, bug analyses, overflow defense specifications, and all seven genuine PowerShell evidence screenshots.

---

## 3. Python Runtime & Dependencies

- **Python Runtime:** Python 3.8+ (Verified on Python 3.12.10, AMD64 Windows)
- **Core Dependencies (`requirements.txt`):**
  - `hypothesis>=6.170.0` (Tested on 6.170.14)
  - `pytest>=9.2.0` (Tested on 9.2.0)
  - `reportlab>=4.0.0`
  - `pymupdf>=1.24.0`

### Installation Instructions:
```powershell
# Navigate to the Lab 7 directory
Set-Location "Lab7_FuzzTesting"

# Install dependencies
python -m pip install -r requirements.txt

# Verify installations
python -m pip show hypothesis pytest
```

---

## 4. Execution & Testing Commands

### Running Individual Test Suites:
```powershell
# Run compatibility wrapper tests (11 property-based tests)
python -m pytest test_processor.py -v

# Run canonical domain tests (11 property-based tests)
python -m pytest test_visa_application.py -v
```

### Running the Complete Test Suite:
```powershell
# Run all tests in the submission folder (22 property-based tests)
python -m pytest -v
```

### Verifying Bytecode Compilation:
```powershell
python -m compileall .
```

### Running the Interactive CLI Application:
```powershell
python processor.py
```

---

## 5. Expected Test & Execution Results

| Command | Expected Result | Verified Timing |
|---|---|---|
| `python -m pytest test_processor.py -v` | **11 passed** (0 failed, 0 skipped) | 1.12s |
| `python -m pytest test_visa_application.py -v` | **11 passed** (0 failed, 0 skipped) | 1.11s |
| `python -m pytest -v` | **22 passed** (0 failed, 0 skipped) | 2.03s |
| `python -m compileall .` | **Exited code 0** (0 syntax errors) | Clean |

### Expected Interactive CLI Validation Results:

- **Valid Input Set:**
  - Visa Type & Entries: `tourist:2` &rarr; `('Tourist', 2)`
  - Processing Days CSV: `5,10,21` &rarr; `12`
  - Fee & Discount: `6000|500` &rarr; `6580.0`
- **Invalid & Overflow Input Set:**
  - Malformed Delimiter: `bad:delimiters` &rarr; `None`
  - Empty CSV Token: `5,,21` &rarr; `None`
  - Arithmetic Overflow: `1.6e308|0` &rarr; `None` (safely contained without crash)

---

## 6. Evidence Screenshots Description

All seven screenshots are genuine Windows PowerShell terminal captures located in `screenshots/` and embedded into `Lab_7_FuzzTesting_Report.pdf`:

| File | Size (Bytes) | Description |
|---|---|---|
| `screenshots/01_environment.png` | 93,323 | Terminal verification of Python 3.12.10, pytest 9.2.0, and hypothesis 6.170.14 |
| `screenshots/02_test_processor.png` | 104,836 | Verbose execution of `test_processor.py` showing all 11 tests passing in 1.12s |
| `screenshots/03_test_visa_application.png` | 104,635 | Verbose execution of `test_visa_application.py` showing all 11 tests passing in 1.11s |
| `screenshots/04_full_test_suite.png` | 167,492 | Full pytest execution showing 22 collected items and 22 passed in 2.03s |
| `screenshots/05_compilation.png` | 43,128 | Clean Python bytecode compilation via `python -m compileall .` exiting with code 0 |
| `screenshots/06_valid_input.png` | 36,097 | Interactive CLI verification with representative valid inputs |
| `screenshots/07_invalid_input.png` | 36,167 | Interactive CLI verification showing safe `None` return on malformed and overflow inputs |

---

## 7. Submission Directory Structure

```text
Lab7_FuzzTesting/
├── processor.py                   # Generic submission wrapper (re-exports canonical SSOT)
├── visa_application.py            # Hardened canonical domain implementation (SSOT)
├── test_processor.py              # 11 Hypothesis fuzz tests (exercises processor.py)
├── test_visa_application.py       # 11 Hypothesis fuzz tests (exercises visa_application.py)
├── pytest.ini                     # Pytest configuration (--import-mode=importlib)
├── requirements.txt               # Package dependencies (hypothesis, pytest, reportlab, pymupdf)
├── README.md                      # Complete project documentation and execution guide
├── FINAL_VERIFICATION_REPORT.md   # Formal verification and audit execution logs
├── Lab_7_FuzzTesting_Report.pdf   # 8-page comprehensive formal PDF report (17 sections)
└── screenshots/                   # Genuine PowerShell desktop evidence captures
    ├── 01_environment.png
    ├── 02_test_processor.png
    ├── 03_test_visa_application.png
    ├── 04_full_test_suite.png
    ├── 05_compilation.png
    ├── 06_valid_input.png
    └── 07_invalid_input.png
```
