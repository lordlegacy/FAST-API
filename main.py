# main.py
from reddit_scrapper import RedditScraper
from database_handler import DatabaseHandler
from image_downloader import ImageDownloader
from scheduler import Scheduler
import os

def process_posts():
    reddit_scraper = RedditScraper()
    db_handler = DatabaseHandler()
    image_downloader = ImageDownloader()

    posts = reddit_scraper.get_recent_posts()
    
    os.makedirs("images", exist_ok=True)
    
    for post in posts:
        file_path = os.path.join("images", f"{post['post_id']}.jpg")
        image_downloader.download_image(post['url'], file_path)

    db_handler.insert_posts(posts)
    db_handler.close()

    print(f"Processed {len(posts)} posts")

def daily_job():
    print("Starting daily job to process posts...")
    process_posts()
    print("Daily job completed.")

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.schedule_job(daily_job, "15:41")
    print("Scheduler started. Waiting for 14:32 to run the daily job...")
    scheduler.run()