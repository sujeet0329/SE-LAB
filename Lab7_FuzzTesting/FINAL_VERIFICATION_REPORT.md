# FINAL VERIFICATION REPORT — LAB 7 FUZZ TESTING WITH HYPOTHESIS

**Student Name:** Sujeet V Bire  
**SRN:** PES1UG24CS716  
**Institution:** Department of Computer Science & Engineering, PES University  
**Assigned Repository:** `https://github.com/SETAPESU26/L6_L7_52_visa_application`  
**Domain Module:** Visa Application System  
**Verified Directory:** `F:\SE 7\Lab7_Submission`  
**Date:** November 2026  
**Operating System:** Windows (AMD64)  
**Python Runtime:** 3.12.10  
**Pytest Version:** 9.2.0  
**Hypothesis Version:** 6.170.14  

---

## 1. Executive Summary & Verification Verdict

- **Canonical Application (`visa_application.py`):** Fully hardened against malformed delimiters, empty strings, invalid types, negative inputs, zero-division, non-finite values (`NaN`, `Inf`), and floating-point arithmetic overflow (`if not math.isfinite(raw_total): return None`).
- **Compatibility Module (`processor.py`):** Explicitly wraps and re-exports all three hardened functions (`parse_application`, `processing_average`, `payable_fee`) and the interactive CLI `main()` from `visa_application.py`.
- **Test Suites (`test_processor.py` & `test_visa_application.py`):** Both test suites implement exactly 11 comprehensive Hypothesis property-based fuzz tests, including the overflow regression test `test_payable_fee_rejects_overflow`.
- **Verified Test Execution within `F:\SE 7\Lab7_Submission`:**
  - `python -m pytest test_processor.py -v`: **11 PASSED in 1.12s** (0 failed, 0 skipped, 11 collected).
  - `python -m pytest test_visa_application.py -v`: **11 PASSED in 1.11s** (0 failed, 0 skipped, 11 collected).
  - `python -m pytest -v`: **22 PASSED in 2.03s** (0 failed, 0 skipped, 22 collected across both modules under rootdir `F:\SE 7\Lab7_Submission`).
- **Python Compilation:** `python -m compileall .` executed inside `F:\SE 7\Lab7_Submission` completed with **0 errors**.
- **CLI Application:** Verified with valid inputs (`tourist:2`, `5,10,21`, `6000|500`) producing `('Tourist', 2)`, `12`, and `6580.0`. Verified with boundary/overflow inputs (`bad:delimiters`, `5,,21`, `1.6e308|0`) returning `None` safely without crashing.
- **Desktop Screenshot Evidence:** All seven genuine Windows PowerShell screenshots were captured directly from the student's interactive desktop station, placed into `F:\SE 7\Lab7_Submission\screenshots\`, validated for non-zero file sizes and aspect ratios, and successfully embedded across Section 16 of the 8-page PDF report.
- **Final Verdict:** **READY FOR SUBMISSION** — All canonical source code, test suites, compilation, CLI validation, 7 genuine screenshots, and 8-page formal PDF report are 100% verified.

---

## 2. Verified Command Execution Logs (Inside `F:\SE 7\Lab7_Submission`)

### A. Environment Verification
```powershell
PS F:\SE 7\Lab7_Submission> Set-Location "F:\SE 7\Lab7_Submission"; Get-Location

Path
----
F:\SE 7\Lab7_Submission

PS F:\SE 7\Lab7_Submission> python --version; python -m pip show pytest hypothesis
Python 3.12.10
Name: pytest
Version: 9.2.0
Summary: pytest: simple powerful testing with Python
Location: C:\Users\sujee\AppData\Local\Programs\Python\Python312\Lib\site-packages
Requires: colorama, iniconfig, packaging, pluggy, pygments
---
Name: hypothesis
Version: 6.170.14
Summary: The property-based testing library for Python
Location: C:\Users\sujee\AppData\Local\Programs\Python\Python312\Lib\site-packages
Requires: sortedcontainers
```

### B. Compatibility Test Suite Execution (`test_processor.py`)
```powershell
PS F:\SE 7\Lab7_Submission> python -m pytest test_processor.py -v
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\sujee\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
hypothesis profile 'default'
rootdir: F:\SE 7\Lab7_Submission
configfile: pytest.ini
plugins: hypothesis-6.170.14, platformdirs-4.12.2
collecting ... collected 11 items

test_processor.py::test_parse_application_no_crash PASSED                [  9%]
test_processor.py::test_processing_average_no_crash PASSED               [ 18%]
test_processor.py::test_payable_fee_no_crash PASSED                      [ 27%]
test_processor.py::test_parse_application_valid_inputs PASSED            [ 36%]
test_processor.py::test_processing_average_valid_inputs PASSED           [ 45%]
test_processor.py::test_payable_fee_valid_inputs PASSED                  [ 54%]
test_processor.py::test_parse_application_invalid_inputs PASSED          [ 63%]
test_processor.py::test_processing_average_invalid_inputs PASSED         [ 72%]
test_processor.py::test_payable_fee_invalid_inputs PASSED                [ 81%]
test_processor.py::test_payable_fee_monotonicity PASSED                  [ 90%]
test_processor.py::test_payable_fee_rejects_overflow PASSED              [100%]

============================= 11 passed in 1.12s ==============================
```

### C. Canonical Test Suite Execution (`test_visa_application.py`)
```powershell
PS F:\SE 7\Lab7_Submission> python -m pytest test_visa_application.py -v
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\sujee\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
hypothesis profile 'default'
rootdir: F:\SE 7\Lab7_Submission
configfile: pytest.ini
plugins: hypothesis-6.170.14, platformdirs-4.12.2
collecting ... collected 11 items

test_visa_application.py::test_parse_application_no_crash PASSED         [  9%]
test_visa_application.py::test_processing_average_no_crash PASSED        [ 18%]
test_visa_application.py::test_payable_fee_no_crash PASSED               [ 27%]
test_visa_application.py::test_parse_application_valid_inputs PASSED     [ 36%]
test_visa_application.py::test_processing_average_valid_inputs PASSED    [ 45%]
test_visa_application.py::test_payable_fee_valid_inputs PASSED           [ 54%]
test_visa_application.py::test_parse_application_invalid_inputs PASSED   [ 63%]
test_visa_application.py::test_processing_average_invalid_inputs PASSED  [ 72%]
test_visa_application.py::test_payable_fee_invalid_inputs PASSED         [ 81%]
test_visa_application.py::test_payable_fee_monotonicity PASSED           [ 90%]
test_visa_application.py::test_payable_fee_rejects_overflow PASSED       [100%]

============================= 11 passed in 1.11s ==============================
```

### D. Full Test Suite Execution (`F:\SE 7\Lab7_Submission`)
```powershell
PS F:\SE 7\Lab7_Submission> python -m pytest -v
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\sujee\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
hypothesis profile 'default'
rootdir: F:\SE 7\Lab7_Submission
configfile: pytest.ini
plugins: hypothesis-6.170.14, platformdirs-4.12.2
collecting ... collected 22 items

test_processor.py::test_parse_application_no_crash PASSED                [  4%]
test_processor.py::test_processing_average_no_crash PASSED               [  9%]
test_processor.py::test_payable_fee_no_crash PASSED                      [ 13%]
test_processor.py::test_parse_application_valid_inputs PASSED            [ 18%]
test_processor.py::test_processing_average_valid_inputs PASSED           [ 22%]
test_processor.py::test_payable_fee_valid_inputs PASSED                  [ 27%]
test_processor.py::test_parse_application_invalid_inputs PASSED          [ 31%]
test_processor.py::test_processing_average_invalid_inputs PASSED         [ 36%]
test_processor.py::test_payable_fee_invalid_inputs PASSED                [ 40%]
test_processor.py::test_payable_fee_monotonicity PASSED                  [ 45%]
test_processor.py::test_payable_fee_rejects_overflow PASSED              [ 50%]
test_visa_application.py::test_parse_application_no_crash PASSED         [ 54%]
test_visa_application.py::test_processing_average_no_crash PASSED        [ 59%]
test_visa_application.py::test_payable_fee_no_crash PASSED               [ 63%]
test_visa_application.py::test_parse_application_valid_inputs PASSED     [ 68%]
test_visa_application.py::test_processing_average_valid_inputs PASSED    [ 72%]
test_visa_application.py::test_payable_fee_valid_inputs PASSED           [ 77%]
test_visa_application.py::test_parse_application_invalid_inputs PASSED   [ 81%]
test_visa_application.py::test_processing_average_invalid_inputs PASSED  [ 86%]
test_visa_application.py::test_payable_fee_invalid_inputs PASSED         [ 90%]
test_visa_application.py::test_payable_fee_monotonicity PASSED           [ 95%]
test_visa_application.py::test_payable_fee_rejects_overflow PASSED       [100%]

============================= 22 passed in 2.03s ==============================
```

### E. Python Bytecode Compilation
```powershell
PS F:\SE 7\Lab7_Submission> python -m compileall .
Listing '.'...
Compiling '.\\build_pdf_report.py'...
Listing '.\\screenshots'...
Compiling '.\\test_processor.py'...
Compiling '.\\test_visa_application.py'...
# Exited with code 0 (Zero errors)
```

### F. Interactive CLI Execution (Valid Inputs)
```text
PS F:\SE 7\Lab7_Submission> python processor.py
==== Running parse_application ====
Enter visa type:entries (e.g. tourist:2): tourist:2
Visa Type and Entries: ('Tourist', 2)

==== Running processing_average ====
Enter processing days as CSV (e.g. 5,10,21): 5,10,21
Average Processing Days: 12

==== Running payable_fee ====
Enter fee|discount (e.g. 6000|500): 6000|500
Payable Fee: 6580.0
```

### G. Interactive CLI Execution (Invalid & Overflow Inputs)
```text
PS F:\SE 7\Lab7_Submission> python processor.py
==== Running parse_application ====
Enter visa type:entries (e.g. tourist:2): bad:delimiters
Visa Type and Entries: None

==== Running processing_average ====
Enter processing days as CSV (e.g. 5,10,21): 5,,21
Average Processing Days: None

==== Running payable_fee ====
Enter fee|discount (e.g. 6000|500): 1.6e308|0
Payable Fee: None
```

---

## 3. Verified Desktop Screenshot Evidence

In strict accordance with academic guidelines:
> *"Never use screenshots from `F:\SE 7` root as proof that the files in `F:\SE 7\Lab7_Submission` passed. Capture genuine screenshots directly from PowerShell. Do not use Python PIL to create terminal screenshots, HTML/SVG terminal mockups, reconstructed terminal output, or synthetic screenshots."*

All 7 genuine screenshots were captured directly from the interactive Windows PowerShell desktop in `F:\SE 7\Lab7_Submission`, verified on disk, and embedded into `Lab_7_FuzzTesting_Report.pdf`:

| # | Filename | Size (Bytes) | Verification Status | Exact Command Captured |
|---|---|---|---|---|
| 1 | `01_environment.png` | 93,323 | Verified | `python --version; python -m pip show pytest hypothesis` |
| 2 | `02_test_processor.png` | 104,836 | Verified | `python -m pytest test_processor.py -v` (11 passed in 1.12s) |
| 3 | `03_test_visa_application.png` | 104,635 | Verified | `python -m pytest test_visa_application.py -v` (11 passed in 1.11s) |
| 4 | `04_full_test_suite.png` | 167,492 | Verified | `python -m pytest -v` (22 passed in 2.03s) |
| 5 | `05_compilation.png` | 43,128 | Verified | `python -m compileall .` (exited code 0) |
| 6 | `06_valid_input.png` | 36,097 | Verified | `python processor.py` (`('Tourist', 2)`, `12`, `6580.0`) |
| 7 | `07_invalid_input.png` | 36,167 | Verified | `python processor.py` (`None` on invalid & overflow) |

---

## 4. Final Verification Sign-Off

- **Report Status:** Compiled cleanly (8 pages, 431 KB, all 17 sections complete).
- **Execution Timings:** 100% synchronized with actual verified runs.
- **Git Repository Target:** `https://github.com/sujeet0329/SE-LAB` (Branch: `lab7-fuzz-testing-final`).
- **Verdict:** **READY FOR SUBMISSION**
