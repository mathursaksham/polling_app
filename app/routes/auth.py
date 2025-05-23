from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..otp_utils import generate_otp, store_otp, validate_otp
from ..email_utils import send_email
from ..database import SessionLocal
from ..models import AllowedEmail

router = APIRouter()

class EmailRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

@router.post("/request-otp")
def request_otp(data: EmailRequest):
    db = SessionLocal()
    allowed = db.query(AllowedEmail).filter_by(email=data.email).first()
    db.close()
    if not allowed:
        raise HTTPException(status_code=403, detail="Email not allowed")
    otp = generate_otp()
    store_otp(data.email, otp)
    send_email(data.email, "Your OTP Code", f"Your OTP is {otp}")
    return {"message": "OTP sent"}

@router.post("/verify-otp")
def verify_otp(data: OTPVerify):
    if validate_otp(data.email, data.otp):
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid OTP")
