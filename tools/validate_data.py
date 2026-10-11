#!/usr/bin/env python3
"""Integrity checks over the exported CSVs.

These are only possible once the data is text: confirm every constraint
referenced by a style recipe or a weighting actually exists in a catalog,
and that no capability label is a near-duplicate. Data gaps (blank
weightings, one-off capabilities) print as non-blocking warnings. Exits
non-zero only on a broken reference, so it can gate a change.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def col(fname, name):
    with (DATA / fname).open() as f:
        return [row[name].strip() for row in csv.DictReader(f) if row[name].strip()]


def main() -> int:
    catalog = set(col("constraints_architectural.csv", "constraint"))
    problems = []

    recipe_constraints = set(col("style_recipes.csv", "constraint"))
    for c in sorted(recipe_constraints - catalog):
        problems.append(f"style recipe references unknown constraint: {c!r}")

    weighting_constraints = set(col("weightings.csv", "constraint"))
    for c in sorted(weighting_constraints - catalog):
        problems.append(f"weighting references unknown constraint: {c!r}")

    caps = col("weightings.csv", "capability")
    folded = {}
    for cap in set(caps):
        folded.setdefault(cap.lower(), []).append(cap)
    for low, variants in folded.items():
        if len(variants) > 1:
            problems.append(f"capability has case-variant duplicates: {variants}")

    # Data gaps are not integrity failures: report them, do not fail on them.
    warnings = []
    with (DATA / "weightings.csv").open() as f:
        wrows = list(csv.DictReader(f))
    blank = [r for r in wrows if not r["modifier"].strip()]
    if blank:
        warnings.append(f"{len(blank)} weighting rows have a note but no modifier value")
    cap_counts = Counter(r["capability"] for r in wrows)
    rare = sorted(c for c, n in cap_counts.items() if n == 1)
    if rare:
        warnings.append(f"capabilities scored only once (likely incomplete): {rare}")

    print(f"catalog: {len(catalog)} constraints | "
          f"recipes ref {len(recipe_constraints)} | weightings ref {len(weighting_constraints)}")
    if warnings:
        print("\nwarnings (data gaps, non-blocking):")
        for w in warnings:
            print(f"  ! {w}")
    if problems:
        print(f"\nFOUND {len(problems)} integrity problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nAll references resolve. Data is internally consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
