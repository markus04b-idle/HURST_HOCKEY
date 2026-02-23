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
