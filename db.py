from sqlalchemy import create_engine, Column, String, Table, MetaData
import pandas as pd

engine = create_engine("sqlite:///resumes.db")
metadata = MetaData()

resume_table = Table('resumes', metadata,
    Column('Name', String),
    Column('Email', String),
    Column('Phone', String),
    Column('Skills', String)
)

metadata.create_all(engine)

def save_to_db(parsed_data):
    df = pd.DataFrame([parsed_data])
    df['Skills'] = df['Skills'].apply(lambda x: ', '.join(x))
    df = df[['Name', 'Email', 'Phone', 'Skills']]
    df.to_sql('resumes', con=engine, if_exists='append', index=False)
