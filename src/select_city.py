"""Pick the city to analyse from the team members' ID numbers.

Rule (course assignment): sum every digit of all IDs, take the sum modulo 26,
map 0->A ... 25->Z, and choose a city from data/airbnb_major_cities.txt that
starts with that letter.

Usage:
    python src/select_city.py                       # interactive
    python src/select_city.py TEAM_MEMBER_1_ID TEAM_MEMBER_2_ID   # IDs as arguments
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITIES_FILE = ROOT / "data" / "airbnb_major_cities.txt"
SELECTED_FILE = ROOT / "data" / "selected_city.txt"


def read_cities(path: Path = CITIES_FILE) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def letter_from_ids(ids: list[str]) -> tuple[int, int, str]:
    """Return (digit_sum, index, letter) for a list of ID strings."""
    total = sum(int(ch) for s in ids for ch in s if ch.isdigit())
    idx = total % 26
    return total, idx, chr(ord("A") + idx)


def cities_for_letter(cities: list[str], letter: str) -> list[str]:
    return sorted(c for c in cities if c.upper().startswith(letter.upper()))


def ask_ids() -> list[str]:
    while True:
        try:
            n = int(input("How many team members? ").strip())
            if n >= 1:
                break
        except ValueError:
            pass
        print("Please enter an integer >= 1.")
    ids = []
    for i in range(1, n + 1):
        while True:
            s = input(f"Enter ID #{i} (digits only): ").strip()
            if s.isdigit():
                ids.append(s)
                break
            print("Invalid ID. Digits only.")
    return ids


def choose(options: list[str]) -> str:
    if len(options) == 1:
        return options[0]
    for i, c in enumerate(options, 1):
        print(f"{i}. {c}")
    lookup = {c.lower(): c for c in options}
    while True:
        raw = input("Choose a city (name or number): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        if raw.lower() in lookup:
            return lookup[raw.lower()]
        print("Invalid choice, try again.")


def main(argv: list[str]) -> None:
    ids = [a for a in argv if a.isdigit()] or ask_ids()
    total, idx, letter = letter_from_ids(ids)
    print(f"Digits sum: {total} | {total} % 26 = {idx} | Letter: {letter}")
    options = cities_for_letter(read_cities(), letter)
    if not options:
        sys.exit(f"No cities start with {letter}.")
    print(f"Cities starting with {letter}: {', '.join(options)}")
    city = choose(options)
    SELECTED_FILE.write_text(city + "\n", encoding="utf-8")
    print(f"Selected city: {city} (saved to {SELECTED_FILE.relative_to(ROOT)})")


if __name__ == "__main__":
    main(sys.argv[1:])
