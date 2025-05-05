import csv

from pathlib import Path

# Base directory where CSVs live (relative to project root)
csv_dir = Path("verification/drc/tables")

# Match all relevant CSV files
csv_files = list(csv_dir.glob("min_drc_*.csv"))

total = 0
for path in csv_files:
    with path.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        count = len(list(reader)) - 1  # Exclude header
        total += count

# Output snippet to be included in the RST
output_path = csv_dir / "_min_drc_rule_count.rst"
with output_path.open("w", encoding="utf-8") as out:
    out.write(f"Total: **{total}**\n")
