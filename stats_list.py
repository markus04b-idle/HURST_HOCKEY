from __future__ import annotations
from pathlib import Path
import csv
from typing import List, Optional

from models import Stats


def _to_int(val: Optional[str]) -> Optional[int]:
    if val is None:
        return None
    v = str(val).strip()
    if v == "":
        return None
    try:
        return int(v)
    except Exception:
        return None


def _to_float(val: Optional[str]) -> Optional[float]:
    if val is None:
        return None
    v = str(val).strip()
    if v == "":
        return None
    try:
        return float(v)
    except Exception:
        return None


def generate_stats(csv_path: Optional[Path | str] = None) -> List[Stats]:
    """Parse `stats.csv` and return a list of `Stats` instances."""
    if csv_path is None:
        csv_path = Path(__file__).parent / "stats.csv"
    csv_path = Path(csv_path)

    stats_list: List[Stats] = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # Player is formatted as "Last, First"
            player = (row.get("Player") or "").strip()
            if "," in player:
                last, first = [s.strip() for s in player.split(",", 1)]
            else:
                parts = player.split()
                first = parts[0] if parts else ""
                last = " ".join(parts[1:]) if len(parts) > 1 else ""

            if not first or not last:
                continue

            number = row.get("Number")
            number = str(number).strip() if number is not None and str(number).strip() != "" else None

            s = Stats(
                first_name=first,
                last_name=last,
                number=number,
                GP=_to_int(row.get("GP")),
                G=_to_int(row.get("G")),
                A=_to_int(row.get("A")),
                PTS=_to_int(row.get("PTS")),
                SH=_to_int(row.get("SH")),
                SH_PCT=_to_float(row.get("SH_PCT")),
                Plus_Minus=_to_int(row.get("Plus_Minus")),
                PPG=_to_int(row.get("PPG")),
                SHG=_to_int(row.get("SHG")),
                FG=_to_int(row.get("FG")),
                GWG=_to_int(row.get("GWG")),
                GTG=_to_int(row.get("GTG")),
                OTG=_to_int(row.get("OTG")),
                HTG=_to_int(row.get("HTG")),
                UAG=_to_int(row.get("UAG")),
                PN_PIM=(row.get("PN-PIM") or None),
                MIN=_to_int(row.get("MIN")),
                MAJ=_to_int(row.get("MAJ")),
                OTH=_to_int(row.get("OTH")),
                BLK=_to_int(row.get("BLK")),
            )
            stats_list.append(s)

    return stats_list
