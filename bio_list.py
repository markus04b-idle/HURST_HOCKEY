from __future__ import annotations
from pathlib import Path
import csv
from typing import List, Optional

from models import Bio


def generate_bios(csv_path: Optional[Path | str] = None) -> List[Bio]:
    """Parse the players CSV and return a list of `Bio` instances.

    The function looks for `players.csv` next to this file by default.
    """
    if csv_path is None:
        csv_path = Path(__file__).parent / "players.csv"
    csv_path = Path(csv_path)

    bios: List[Bio] = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            first = (row.get("First Name") or "").strip()
            last = (row.get("Last Name") or "").strip()
            if not first or not last:
                continue

            # Number and weight may fail conversion; fall back to None
            number = None
            weight = None
            try:
                num_val = row.get("Number")
                if num_val and num_val.strip() != "":
                    number = int(num_val)
            except Exception:
                number = None
            try:
                w_val = row.get("Weight")
                if w_val and w_val.strip() != "":
                    weight = int(w_val)
            except Exception:
                weight = None

            position = (row.get("Position") or "").strip() or None
            height = (row.get("Height") or "").strip() or None
            academic_class = (row.get("Class") or "").strip() or None
            hometown = (row.get("Hometown") or "").strip() or None
            high_school = (row.get("High School") or "").strip() or None

            bio = Bio(
                first_name=first,
                last_name=last,
                number=number,
                position=position,
                height=height,
                weight=weight,
                academic_class=academic_class,
                hometown=hometown,
                high_school=high_school,
            )
            bios.append(bio)

    return bios
