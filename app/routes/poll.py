from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..database import SessionLocal
from ..models import Poll, Option, Vote
from ..email_utils import send_email

router = APIRouter()

class VoteRequest(BaseModel):
    email: EmailStr
    poll_id: int
    option_id: int

@router.get("/")
def get_polls():
    db = SessionLocal()
    polls = db.query(Poll).all()
    db.close()
    return [{"id": p.id, "title": p.title, "description": p.description} for p in polls]

@router.post("/vote")
def cast_vote(vote: VoteRequest):
    db = SessionLocal()
    existing = db.query(Vote).filter_by(email=vote.email, poll_id=vote.poll_id).first()
    if existing:
        db.close()
        raise HTTPException(status_code=409, detail="You have already voted on this poll")
    new_vote = Vote(email=vote.email, poll_id=vote.poll_id, option_id=vote.option_id)
    db.add(new_vote)
    db.commit()
    db.close()
    send_email(vote.email, "Vote Confirmation", f"Your vote for poll {vote.poll_id} has been recorded.")
    return {"message": "Vote cast successfully"}
