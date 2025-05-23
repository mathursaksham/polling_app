import random
from datetime import datetime, timedelta
from .database import SessionLocal
from .models import OTPStore

def generate_otp():
    return f"{random.randint(100000, 999999)}"

def store_otp(email: str, otp: str):
    db = SessionLocal()
    db.query(OTPStore).filter(OTPStore.email == email).delete()
    db.commit()
    db.add(OTPStore(email=email, otp=otp))
    db.commit()
    db.close()

def validate_otp(email: str, otp: str) -> bool:
    db = SessionLocal()
    entry = db.query(OTPStore).filter_by(email=email, otp=otp).first()
    if entry and (datetime.utcnow() - entry.created_at < timedelta(minutes=10)):
        db.query(OTPStore).filter_by(email=email).delete()
        db.commit()
        db.close()
        return True
    db.close()
    return False
