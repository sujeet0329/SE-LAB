# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and coding-style problems. It helps developers detect issues early, improve maintainability, and make software safer and more reliable.

## 2. What differences did you observe between Pylint, Bandit, and Flake8?

Pylint checks overall code quality, naming conventions, documentation, and potential programming errors. Bandit focuses on security vulnerabilities, such as unsafe eval() usage, weak hashing, and shell command execution. Flake8 identifies style violations, unused imports, unused variables, and formatting problems. Using all three provides broader coverage than relying on a single tool.

## 3. Which issues did you prioritize, and how did you fix them?

I prioritized security issues, including unsafe eval() usage, weak MD5 hashing, shell command execution, insecure OTP generation, and hardcoded secrets. I replaced unsafe expression evaluation with validated numeric discount calculations, used SHA-256 hashing and the secrets module, removed shell execution, and read the registrar token from an environment variable. I also fixed the mutable default argument, exception handling, file management, naming, and formatting issues.

## 4. What are the limitations of static code analysis?

Static analysis tools can identify many common problems, but they cannot guarantee that a program is completely correct or secure. They may miss runtime errors, business-logic defects, and vulnerabilities that depend on the execution environment. Therefore, static analysis should be combined with testing, code review, and appropriate security practices.
