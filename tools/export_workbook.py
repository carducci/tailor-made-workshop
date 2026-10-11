#!/usr/bin/env python3
"""Export the Architecture workbook's data tables to plain-text CSV.

Why this exists: the model (constraints, capabilities, per-pair weightings,
style recipes) lives inside a binary .xlsx, so every change is an
unreviewable diff, and identifiers retyped by hand across tabs accumulate
typos (mostly consistent, so harmless to joins today, but unreadable and a
latent risk). This reads the workbook once, applies a single consistent
spelling map, and writes clean CSVs that git can diff. Run it to regenerate
data/ from the xlsx; review the printed report for what the spelling map changed.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

import openpyxl

# One spelling map, applied to every string cell so a renamed identifier
# stays consistent across all sheets (otherwise a cross-sheet join breaks).
# Substring, case-sensitive: each key is unambiguous.
SPELLING = {
    "Arithmatic": "Arithmetic",       # combination-behavior key, 200+ cells
    "Databse": "Database",            # inside the "Decoupled Databse" id, 13 cells
    "Goverance": "Governance",
    "Independend": "Independent",
    "interoperabilty": "interoperability",
    "volitile": "volatile",
    "bevavior": "behavior",
}

# Capability labels that differ only by case are the same criterion.
CAPABILITY_CANON = {"workflow": "Workflow", "cost": "Cost"}

# Rows whose key cell is a leaked header, dropped on export.
HEADER_LEAKS = {"Capability", "Constraint"}


def fix(value):
    if not isinstance(value, str):
        return value
    out = value
    for bad, good in SPELLING.items():
        out = out.replace(bad, good)
    return out.strip()


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    xlsx = root / "Architecture workbook.xlsx"
    out = root / "data"
    out.mkdir(exist_ok=True)
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    report: Counter = Counter()

    def write_csv(fname, header, rows):
        with (out / fname).open("w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(header)
            w.writerows(rows)
        print(f"  wrote data/{fname}  ({len(rows)} rows)")

    # 1) Master weightings: Constraint x Capability -> Modifier (+ metadata)
    ws = wb["Constraint Weightings"]
    rows = []
    for r in ws.iter_rows(min_row=2, max_col=7, values_only=True):
        constraint = fix(r[0])
        if not constraint or constraint in HEADER_LEAKS:
            continue
        cap = fix(r[1])
        if cap in HEADER_LEAKS:
            continue
        if cap in CAPABILITY_CANON:
            report[f"capability '{cap}' -> '{CAPABILITY_CANON[cap]}'"] += 1
            cap = CAPABILITY_CANON[cap]
        rows.append([constraint, cap, fix(r[2]) or "", fix(r[3]) or "",
                     fix(r[4]) or "", r[5] if r[5] is not None else "", fix(r[6]) or ""])
    write_csv("weightings.csv",
              ["constraint", "capability", "dominant", "class", "behavior", "modifier", "notes"],
              rows)

    # 2) The four constraint catalogs
    catalogs = {
        "Architectural Constraints": ("constraints_architectural.csv", ["constraint", "class"]),
        "Team Constraints": ("constraints_team.csv", ["constraint", "formal_name", "description"]),
        "Organizational Constraints": ("constraints_organizational.csv", ["constraint", "formal_name", "description"]),
        "Environmental Constraints": ("constraints_environmental.csv", ["constraint", "formal_name", "description"]),
    }
    for sheet, (fname, header) in catalogs.items():
        ws = wb[sheet]
        rows = []
        for r in ws.iter_rows(min_row=2, max_col=len(header), values_only=True):
            if not r[0] or fix(r[0]) in HEADER_LEAKS:
                continue
            rows.append([fix(v) or "" for v in r[:len(header)]])
        write_csv(fname, header, rows)

    # 3) Style recipes: style -> constraint
    ws = wb["Abstract Styles"]
    rows = []
    for r in ws.iter_rows(min_row=2, max_col=2, values_only=True):
        if not r[0] or fix(r[0]) in HEADER_LEAKS:
            continue
        rows.append([fix(r[0]), fix(r[1]) or ""])
    write_csv("style_recipes.csv", ["style", "constraint"], rows)

    # Count every spelling substitution actually made, across all sheets.
    for sheet in wb.sheetnames:
        for row in wb[sheet].iter_rows(values_only=True):
            for v in row:
                if isinstance(v, str):
                    for bad in SPELLING:
                        if bad in v:
                            report[f"spelling '{bad}' -> '{SPELLING[bad]}'"] += v.count(bad)

    print("\n--- change report ---")
    for k, n in report.most_common():
        print(f"  {k}: {n} cells")
    return 0


if __name__ == "__main__":
    sys.exit(main())
