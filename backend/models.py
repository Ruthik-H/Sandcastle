
from sqlalchemy import Column, Integer, String
from database import Base

class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True, index=True)
    repository = Column(String, nullable=False)
    pull_request = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
