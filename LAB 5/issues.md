# Lab 5: Static Code Analysis — Issues and Fixes

| Issue | Type | Line(s) Before Fix | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command execution using os.system | Security — High | 63 | Builds and executes a shell command using a filename, which may allow command injection. | Remove shell execution and print the export message directly. |
| Weak MD5 hash | Security — High | 52 | MD5 is unsuitable for security-sensitive hashing. | Replace MD5 with SHA-256. |
| Dynamic eval() execution | Security — Medium | 47 | eval() executes an arbitrary expression and may execute malicious code. | Calculate the scholarship fee using validated numeric inputs instead. |
| Mutable default argument | Code quality | 15 | The default audit_trail list is shared between function calls. | Use None as the default and create a new list when needed. |
| Bare except clause | Code quality/Security | 31 | Suppresses every exception, hiding unexpected errors. | Catch the specific expected exception and handle it explicitly. |
| Insecure OTP generation | Security — Low | 56 | random.randint() is not suitable for security-sensitive OTPs. | Use the secrets module to generate the OTP. |
| Hardcoded registrar token | Security | 75 | A secret is embedded in the source code and printed. | Read the token from an environment variable and never print its value. |
| File handling without a context manager | Code quality | 60–61 | The file may not close properly if an error occurs. | Use a with statement and specify UTF-8 encoding. |
| Unused import and variables | Code quality | 4, 36, 46 | math, lab_fee and base_fee are unused. | Remove unused code. |
| Naming, formatting and documentation issues | Style | Multiple | Missing docstrings, non-snake_case function names, long lines and missing final newline. | Use PEP 8 naming, docstrings, shorter lines and a final newline. |
| Incorrect scholarship calculation design | Logic/Security | 45–48 | The function evaluates a string instead of calculating a validated discount from the course fee. | Accept a numeric discount rate and calculate the fee directly. |
