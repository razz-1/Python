#!/usr/bin/env python3
"""
Password Generator
-------------------
Generates one or more cryptographically secure random passwords.

Usage examples:
    python password_generator.py
    python password_generator.py --length 20 --count 5
    python password_generator.py --no-symbols
    python password_generator.py --length 16 --no-ambiguous
"""

import argparse
import secrets
import string


AMBIGUOUS_CHARS = "il1Lo0O"


def build_char_pool(use_lower, use_upper, use_digits, use_symbols, exclude_ambiguous):
    """Build the pool of characters to choose from based on selected options."""
    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%^&*()-_=+[]{};:,.<>?/"

    if not pool:
        raise ValueError("At least one character set must be enabled.")

    if exclude_ambiguous:
        pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARS)

    return pool


def generate_password(length, pool, require_all_sets=None):
    """Generate a single secure password of the given length from the pool."""
    if length < 4:
        raise ValueError("Password length should be at least 4 for reasonable security.")

    password = [secrets.choice(pool) for _ in range(length)]

    # If specific character sets must each appear at least once, enforce it.
    if require_all_sets:
        for i, char_set in enumerate(require_all_sets):
            if char_set and not any(c in char_set for c in password):
                # Replace a random position with a char from the missing set
                pos = secrets.randbelow(length)
                password[pos] = secrets.choice(char_set)

    return "".join(password)


def password_strength_label(length, pool_size):
    """Rough qualitative strength estimate based on entropy bits."""
    import math
    entropy_bits = length * math.log2(pool_size)
    if entropy_bits < 40:
        return "Weak"
    elif entropy_bits < 60:
        return "Moderate"
    elif entropy_bits < 80:
        return "Strong"
    else:
        return "Very Strong"


def main():
    parser = argparse.ArgumentParser(description="Generate secure random passwords.")
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length (default: 16)")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate (default: 1)")
    parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase letters")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--no-ambiguous", action="store_true", help="Exclude ambiguous characters (l, 1, I, O, 0, etc.)")

    args = parser.parse_args()

    use_lower = not args.no_lower
    use_upper = not args.no_upper
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols

    pool = build_char_pool(use_lower, use_upper, use_digits, use_symbols, args.no_ambiguous)

    # Build list of char sets that must appear at least once (for enforced diversity)
    required_sets = []
    if use_lower:
        required_sets.append(string.ascii_lowercase)
    if use_upper:
        required_sets.append(string.ascii_uppercase)
    if use_digits:
        required_sets.append(string.digits)
    if use_symbols:
        required_sets.append("!@#$%^&*()-_=+[]{};:,.<>?/")

    print(f"\nGenerating {args.count} password(s) of length {args.length}\n" + "-" * 40)
    for _ in range(args.count):
        pwd = generate_password(args.length, pool, required_sets)
        strength = password_strength_label(args.length, len(pool))
        print(f"{pwd}   [{strength}]")
    print()


if __name__ == "__main__":
    main()