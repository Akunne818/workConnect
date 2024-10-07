import sqlalchemy
import models
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Text
from sqlalchemy.sql import func

from models.base_models import Base, Basemodels


class Job(Basemodels, Base):
    __tablename__ = 'jobs'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    if models.storage_t == "db":
        title = Column(String(250), nullable=False)
        description = Column(Text)
        salary = Column(Integer)
        categories = Column(String(250))
        location = Column(String(250))
        employer_id = Column(String(250), ForeignKey('employers.id'))
        applicants = Column(String(250), default=[])

    