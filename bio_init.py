from sqlmodel import Session
from models import engine
from bio_list import generate_bios

with Session(engine) as session:
    bios = generate_bios()
    session.add_all(bios)
    session.commit()