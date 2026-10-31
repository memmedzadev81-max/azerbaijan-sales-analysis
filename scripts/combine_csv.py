"""CSV hissələrini birləşdir"""
from pathlib import Path
base = Path(__file__).resolve().parent.parent / "data"
p1 = (base / "sales_part1.csv").read_text(encoding="utf-8")
p2 = (base / "sales_part2.csv").read_text(encoding="utf-8")
# part1 already has header
out = p1.rstrip("\n") + "\n" + p2.lstrip("\n")
(base / "sales_data.csv").write_text(out, encoding="utf-8")
print(f"Combined: {len(out.splitlines())} lines -> data/sales_data.csv")
