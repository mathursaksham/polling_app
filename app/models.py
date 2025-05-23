from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class AllowedEmail(Base):
    __tablename__ = 'allowed_emails'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)

class OTPStore(Base):
    __tablename__ = 'otp_store'
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    otp = Column(String(6))
    created_at = Column(DateTime, default=datetime.utcnow)

class Poll(Base):
    __tablename__ = 'polls'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(1024))
    options = relationship("Option", back_populates="poll")

class Option(Base):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('polls.id'))
    text = Column(String(255))
    poll = relationship("Poll", back_populates="options")

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    poll_id = Column(Integer, ForeignKey('polls.id'))
    option_id = Column(Integer, ForeignKey('options.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('email', 'poll_id', name='_user_poll_uc'),)
