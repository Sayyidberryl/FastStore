from sqlalchemy.orm import Session
from ..models.user import Users

class UserRepository():
    def __init__(self, db: Session):
        self.db = db
        
    def get_all(self):
        return self.db.query(Users).all()
    
    def get_by_id(self, id):
        return self.db.query(Users).filter(Users.id == id).first()
    def get_by_username(self, username):
        return self.db.query(Users).filter(Users.username == username).first()
    
    def add_user(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, user: Users):
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user: Users):
        self.db.delete(user)
        self.db.commit()
        return user