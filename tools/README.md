# Workbook tools

Scripts that turn `Architecture workbook.xlsx` into reviewable text.

The workbook remains the source of truth. The CSVs under `data/` are a
generated view of it, so changes show up as readable git diffs and a script
can check the data for consistency. Regenerate them whenever the workbook
changes.

## Requirements

Python 3 and `openpyxl`:

```
pip install openpyxl
```

## Usage

```
python3 tools/export_workbook.py    # xlsx -> data/*.csv, prints a change report
python3 tools/validate_data.py      # integrity checks; exits non-zero on a broken reference
```

`export_workbook.py` reads the workbook's cached values, applies one spelling
map consistently across every sheet (so a renamed identifier stays joinable),
and writes the catalogs, the per-pair weightings, and the style recipes.
`validate_data.py` confirms every constraint a recipe or weighting references
exists in a catalog, and reports data gaps (blank weightings, one-off
capabilities) as warnings.
