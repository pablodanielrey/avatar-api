from model_utils import Base
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, or_

class Avatar(Base):

    __tablename__ = 'avatar'

    data = Column(String)
    content_type = Column(String)
    hash = Column(String)