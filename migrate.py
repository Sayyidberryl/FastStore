"""
Database Migration Script
Run this script to create all tables in the database
"""

from app.core.database import engine, Base
from app.models.user import User
from app.models.category import Category
from app.models.product import Product

def create_tables():
    """Create all tables in the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        print("Tables created:")
        print("- users")
        print("- categories") 
        print("- products")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()