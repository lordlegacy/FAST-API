# database.py
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_PARAMS

# Database setup
DATABASE_URL = f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, unique=True, index=True)
    title = Column(String)
    url = Column(String)
    file_path = Column(String)
    posted_time = Column(DateTime)

# Create the database tables
Base.metadata.create_all(bind=engine)

def save_image_to_db(post_data):
    db = SessionLocal()
    try:
        existing_image = db.query(Image).filter(Image.post_id == post_data['post_id']).first()
        
        if existing_image:
            existing_image.title = post_data['title']
            existing_image.url = post_data['url']
            existing_image.file_path = os.path.join("images", f"{post_data['post_id']}.jpg")
            existing_image.posted_time = post_data['posted_time']
            print(f"Updated existing image: {post_data['post_id']}")
        else:
            new_image = Image(
                post_id=post_data['post_id'],
                title=post_data['title'],
                url=post_data['url'],
                file_path=os.path.join("images", f"{post_data['post_id']}.jpg"),
                posted_time=post_data['posted_time']
            )
            db.add(new_image)
            print(f"Added new image: {post_data['post_id']}")
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error saving image to database: {e}")
    finally:
        db.close()
