# main.py
from reddit_scrapper import RedditScraper
from image_downloader import ImageDownloader
from database import save_image_to_db
import os

def process_posts():
    reddit_scraper = RedditScraper()
    image_downloader = ImageDownloader()
    posts = reddit_scraper.get_recent_posts()
    
    os.makedirs("images", exist_ok=True)
    
    for post in posts:
        file_path = os.path.join("images", f"{post['post_id']}.jpg")
        image_downloader.download_image(post['url'], file_path)
        save_image_to_db(post)

    print(f"Processed {len(posts)} posts")

def daily_job():
    print("Starting daily job to process posts...")
    process_posts()
    print("Daily job completed.")

if __name__ == "__main__":
    daily_job()