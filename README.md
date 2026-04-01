# 🔐 Password Strength Checker

A command-line tool that analyses the strength of a password and gives actionable feedback all in a single Python file with no external dependencies.

## Features

- Scores passwords from 0–100
- Rates strength as **Weak**, **Fair**, **Strong**, or **Very Strong**
- Checks for:
  - Minimum length (8 characters required, 12+ recommended)
  - Uppercase and lowercase letters
  - Numbers
  - Special characters (`! @ # $ % & * ` etc.)
  - Repeated characters (`aaa`, `111`)
  - Sequential patterns (`1234`, `abcd`, `qwerty`)
  - Common/leaked passwords (e.g. `password123`, `letmein`)
- Provides clear suggestions for improvement
- Password input is hidden (not echoed to terminal)
- No external dependencies as it uses just the Python standard libraries

## Demo

```
🔐 Password Strength Checker
Enter a password to check:

────────────────────────────────────────
  Strength : Very Strong
  Score    : 95/100
────────────────────────────────────────

✔ Passed:
   ✔ Length: 16+ characters (excellent)
   ✔ Contains uppercase letters
   ✔ Contains lowercase letters
   ✔ Contains numbers
   ✔ Contains special characters
```

## Getting Started

No installation required — just Python 3.

```bash
git clone https://github.com/ajchurch/password-strength-checker.git
cd password-strength-checker
python main.py
```

You'll be prompted to enter a password securely (input is hidden).

## Usage

### Interactive (recommended)
```bash
python main.py
```

### Pass password as argument (for testing/scripting)
```bash
python main.py "MyP@ssword123!"
```

## How Scoring Works

| Check | Points |
|---|---|
| 16+ characters | +30 |
| 12–15 characters | +20 |
| 8–11 characters | +10 |
| Uppercase letters | +15 |
| Lowercase letters | +15 |
| Numbers | +15 |
| Special characters | +20 |
| Repeated characters (e.g. `aaa`) | −10 |
| Sequential patterns (e.g. `1234`) | −10 |
| Common password match | Score = 0 |

| Score | Strength |
|---|---|
| 80–100 | Very Strong |
| 60–79 | Strong |
| 40–59 | Fair |
| 0–39 | Weak |

## Security Notes

- Passwords entered interactively are never stored or logged as all checks are run locally. 
