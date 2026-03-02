from sqlmodel import Session, select
from models import engine, Bio, Stats
import pandas as pd

with Session(engine) as session:
    statement = (
        select(Bio.first_name, Bio.last_name, Bio.position)
        .order_by(Bio.position, Bio.last_name)
    )
    records = session.exec(statement).all()
    
records_df = pd.DataFrame(records)
print(records_df)