from sqlmodel import Session, select
from models import engine, Bio, Stats
import pandas as pd
from sqlalchemy import func

with Session(engine) as session:


    statement = (
        select(Bio.position, Bio.last_name)
        .group_by(Bio.position, Bio.last_name)
    )
    records = session.exec(statement).all()
    
records_df = pd.DataFrame(records)
print(records_df)
