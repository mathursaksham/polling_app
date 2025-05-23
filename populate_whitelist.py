import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import AllowedEmail, Base
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB")

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Replace with your list of allowed emails
emails = ["mathursaksham@gmail.com"]

def populate_whitelist():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    for email in emails:
        if not session.query(AllowedEmail).filter_by(email=email).first():
            session.add(AllowedEmail(email=email))
    session.commit()
    session.close()
    print("Whitelist populated.")

if __name__ == "__main__":
    populate_whitelist()
