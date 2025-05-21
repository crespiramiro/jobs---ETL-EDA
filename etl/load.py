import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

def load_all_jobs_to_db():
    
    df = pd.read_csv("data/processed/all_jobs.csv")

    if not os.path.exists("data/processed/all_jobs.csv"):
        raise FileNotFoundError("The file all_jobs.csv was not found in 'data/processed''.")

    df = df.rename(columns={"jobTitle":"jobtitle","companyName":"companyname","pubDate":"pubdate"})

    try:
     engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
     df.to_sql("all_jobs", engine, if_exists="replace", index=False, schema='jobs')
     print(f"{len(df)} records loaded into the 'all_jobs' table'.")
    except Exception as e:
     print("Error loading data into the database:", e)


if __name__ == "__main__":
    load_all_jobs_to_db()
