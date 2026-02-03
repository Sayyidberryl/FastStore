from sqlalchemy.orm import Session
from ..models.user import User

class UserRepository():
    def __init__(self, db: Session):
        self.db = db
        
    def get_all(self):
        return self.db.query(User).all()
    
    def get_by_id(self, id):
        return self.db.query(User).filter(User.id == id).first()
    
    def add_user(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
        return user