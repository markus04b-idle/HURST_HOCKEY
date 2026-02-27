from sqlmodel import Session
from models import engine
from stats_list import generate_stats

with Session(engine) as session:
    stats = generate_stats()
    session.add_all(stats)
    session.commit()