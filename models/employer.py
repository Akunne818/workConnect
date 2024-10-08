import sqlalchemy
import models
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Text
from sqlalchemy.sql import func

from models.base_models import Base, Basemodels


class Employer(Basemodels, Base):
    __tablename__ = 'employers'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    if models.storage_t == "db":
        email = Column(String(250), nullable=False)
        hashed_password = Column(String(250), nullable=False)
        session_id = Column(String(250), nullable=True)
        reset_token = Column(String(250), nullable=True)
        company_name = Column(String(100), nullable=False)
        first_name = Column(String(100), nullable=False)
        last_name = Column(String(100), nullable=False)
        phone_number = Column(String(20))
        last_login_at = Column(DateTime(timezone=True),
                               server_default=func.now(), onupdate=func.now())
        account_status = Column(String(20))
        description = Column(Text)
        profile_image = Column(String(250))

    
