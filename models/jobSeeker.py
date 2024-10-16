from models.base_models import Basemodels, Base
import sqlalchemy
import models
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Text
from sqlalchemy.sql import func


class JobSeeker(Basemodels, Base):
    __tablename__ = 'job_seekers'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if models.storage_t == "db":
        email = Column(String(250), nullable=False)
        hashed_password = Column(String(250), nullable=False)
        session_id = Column(String(250), nullable=True)
        reset_token = Column(String(250), nullable=True)
        username = Column(String(100), nullable=False)
        state = Column(String(250))
        city = Column(String(250))
        description = Column(Text)
        profile_image = Column(String(250))
        phone_number = Column(String(20))
        last_login_at = Column(DateTime(timezone=True),
                               server_default=func.now(), onupdate=func.now())
        account_status = Column(String(20))
        cv = Column(String(250))
        skills = Column(String(250))
        experience = Column(Integer)

    
