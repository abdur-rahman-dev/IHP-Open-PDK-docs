import csv

from pathlib import Path

# Get absolute path relative to this script file
script_dir = Path(__file__).parent.resolve()
csv_dir = (script_dir / "../verification/drc/tables").resolve()

# Match all relevant CSV files
csv_files = list(csv_dir.glob("min_drc_*.csv"))

total = 0
for path in csv_files:
    with path.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        count = len(list(reader))
        total += count

# Output snippet to be included in the RST
output_path = csv_dir / "_min_drc_rule_count.rst"
with output_path.open("w", encoding="utf-8") as out:
    out.write(f"Total: **{total}**\n")
