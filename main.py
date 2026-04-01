import re
import os
import getpass
import sys

# ── Colour codes ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

STRENGTH_COLOURS = {
    "Weak":        RED,
    "Fair":        YELLOW,
    "Strong":      GREEN,
    "Very Strong": CYAN,
}


# ── Common passwords ──────────────────────────────────────────────────────────
COMMON_PASSWORDS = {
    "password", "password123", "123456", "123456789", "12345678", "12345",
    "1234567", "qwerty", "abc123", "monkey", "111111", "letmein", "dragon",
    "master", "sunshine", "princess", "welcome", "shadow", "superman",
    "michael", "football", "baseball", "soccer", "charlie", "donald",
    "password1", "iloveyou", "admin", "login", "hello", "welcome1",
    "passw0rd", "qwerty123", "starwars", "trustno1", "batman", "mustang",
    "access", "000000", "654321", "987654321",
}

# Common dictionary words that make a password predictable
DICTIONARY_WORDS = {
    "password", "welcome", "monkey", "dragon", "master", "sunshine",
    "princess", "shadow", "superman", "football", "baseball", "soccer",
    "batman", "mustang", "letmein", "trustno", "starwars", "qwerty",
    "admin", "login", "hello", "access", "computer", "internet", "summer",
    "winter", "spring", "autumn", "january", "february", "march", "april",
    "august", "september", "october", "november", "december",
}

# Leet-speak substitution map (normalise before checking dictionary words)
LEET_MAP = str.maketrans({
    "@": "a", "4": "a",
    "3": "e",
    "1": "i", "!": "i",
    "0": "o",
    "5": "s", "$": "s",
    "7": "t",
    "+": "t",
})

def _normalise(password: str) -> str:
    """Lowercase and strip leet-speak substitutions."""
    return password.lower().translate(LEET_MAP)

# ── Core logic ────────────────────────────────────────────────────────────────
def check_password(password: str) -> dict:
    passed = []
    failed = []
    suggestions = []
    score = 0

    normalised = _normalise(password)

    if password.lower() in COMMON_PASSWORDS:
        return {
            "score": 0,
            "strength": "Weak",
            "passed": [],
            "failed": ["Password is extremely common"],
            "suggestions": ["Choose a unique password — this one appears on every hacker's list."],
        }

    length = len(password)
    if length >= 16:
        score += 30
        passed.append("Length: 16+ characters (excellent)")
    elif length >= 12:
        score += 20
        passed.append("Length: 12–15 characters (good)")
    elif length >= 8:
        score += 10
        passed.append("Length: 8–11 characters (minimum)")
        suggestions.append("Use 12 or more characters for a stronger password.")
    else:
        failed.append("Too short (minimum 8 characters)")
        suggestions.append("Your password must be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 15
        passed.append("Contains uppercase letters")
    else:
        failed.append("No uppercase letters")
        suggestions.append("Add at least one uppercase letter (A–Z).")

    if re.search(r"[a-z]", password):
        score += 15
        passed.append("Contains lowercase letters")
    else:
        failed.append("No lowercase letters")
        suggestions.append("Add at least one lowercase letter (a–z).")

    if re.search(r"\d", password):
        score += 15
        passed.append("Contains numbers")
    else:
        failed.append("No numbers")
        suggestions.append("Include at least one number (0–9).")

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", password):
        score += 20
        passed.append("Contains special characters")
    else:
        failed.append("No special characters")
        suggestions.append("Add a special character like !, @, #, $, or %.")

    if re.search(r"(.)\1{2,}", password):
        score -= 10
        failed.append("Contains repeated characters (e.g. 'aaa' or '111')")
        suggestions.append("Avoid repeating the same character more than twice in a row.")

    for seq in ["0123456789", "abcdefghijklmnopqrstuvwxyz", "qwertyuiopasdfghjklzxcvbnm"]:
        for i in range(len(seq) - 3):
            if seq[i:i+4] in password.lower():
                score -= 10
                failed.append("Contains a sequential pattern (e.g. '1234' or 'abcd')")
                suggestions.append("Avoid sequences like '1234', 'abcd', or keyboard patterns.")
                break

    # Dictionary word check (catches leet-speak too, e.g. P@ssw0rd → password)
    matched_word = next((w for w in DICTIONARY_WORDS if w in normalised), None)
    if matched_word:
        score -= 35
        failed.append(f"Based on a common word ('{matched_word}')")
        suggestions.append("Don't base your password on a dictionary word, even with letter substitutions like @ for a or 0 for o.")

    score = max(0, min(score, 100))

    if score >= 80:
        strength = "Very Strong"
    elif score >= 60:
        strength = "Strong"
    elif score >= 40:
        strength = "Fair"
    else:
        strength = "Weak"

    return {
        "score": score,
        "strength": strength,
        "passed": passed,
        "failed": failed,
        "suggestions": list(dict.fromkeys(suggestions)),
    }

# ── Display ───────────────────────────────────────────────────────────────────
def print_report(result: dict) -> None:
    colour = STRENGTH_COLOURS[result["strength"]]

    print()
    print(f"{BOLD}{'─' * 40}{RESET}")
    print(f"  Strength : {colour}{BOLD}{result['strength']}{RESET}")
    print(f"  Score    : {colour}{result['score']}/100{RESET}")
    print(f"{BOLD}{'─' * 40}{RESET}")

    if result["passed"]:
        print(f"\n{GREEN}✔ Passed:{RESET}")
        for item in result["passed"]:
            print(f"   {GREEN}✔{RESET} {item}")

    if result["failed"]:
        print(f"\n{RED}✘ Issues:{RESET}")
        for item in result["failed"]:
            print(f"   {RED}✘{RESET} {item}")

    if result["suggestions"]:
        print(f"\n{YELLOW}💡 Suggestions:{RESET}")
        for tip in result["suggestions"]:
            print(f"   • {tip}")

    print()

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{BOLD}🔐 Password Strength Checker{RESET}")
    print("Your input is never stored or transmitted.\n")

    password = sys.argv[1] if len(sys.argv) > 1 else getpass.getpass("Enter a password to check: ")

    if not password:
        print(f"{RED}No password entered. Exiting.{RESET}")
        sys.exit(1)

    print_report(check_password(password))

