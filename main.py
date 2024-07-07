from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from datetime import datetime
import traceback

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Serve static files (images)
app.mount("/images", StaticFiles(directory="images"), name="images")

# Serve static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "wearelegion",
    "host": "localhost",
    "port": "5432"
}

class ImageMetadata(BaseModel):
    id: str
    title: str
    posted_time: str

@app.get("/api/images", response_model=List[ImageMetadata])
async def get_images():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT post_id as id, title, posted_time FROM reddit_posts ORDER BY posted_time DESC")
        images = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert posted_time to string
        for image in images:
            image['posted_time'] = image['posted_time'].isoformat()
        
        return images
    except Exception as e:
        logger.error(f"Error in /api/images: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')