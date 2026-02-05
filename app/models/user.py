from sqlalchemy import Column, Integer, String, Enum
from ..core.database import Base
import enum

class Roles(str, enum.Enum):
    user = "user"
    admin = "admin"
    seller = "seller"
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(Roles), default=Roles.user, nullable=False)
    