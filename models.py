from sqlmodel import SQLModel, Field

class Bio(SQLModel, table=True):
    first_name: str = Field(primary_key = True)
    last_name: str = Field(primary_key = True)
    number: int | None = None
    position: str | None = None
    height: str | None = None
    weight: int | None = None
    academic_class: str | None = None
    hometown: str | None = None
    high_school: str | None = None

class Stats(SQLModel, table=True):
    first_name: str = Field(primary_key=True, foreign_key="bio.first_name")
    last_name: str = Field(primary_key=True, foreign_key="bio.last_name")
    GP: int | None = None
    G: int | None = None
    A: int | None = None
    PTS: int | None = None
    SH: int | None = None
    SH_PCT: float | None = None
    Plus_Minus: int | None = None
    PPG: int | None = None
    SHG: int | None = None
    FG: int | None = None
    GWG: int | None = None
    GTG: int | None = None
    OTG: int | None = None
    HTG: int | None = None
    UAG: int | None = None
    PN_PIM: str | None = None
    MIN: int | None = None
    MAJ: int | None = None
    OTH: int | None = None
    BLK: int | None = None
