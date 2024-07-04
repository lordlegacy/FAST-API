import praw
import requests
import os
import schedule
import time
from datetime import timedelta
import datetime

# Reddit API authentication
reddit = praw.Reddit(
    client_id="client_id",
    client_secret="client_secret",
    user_agent="myredditapp by /u/yourusername",
)

def download_image(url, file_path):
    """Download an image from a URL and save it to the specified path."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded image: {file_path}")
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")

def process_posts():
    """Process posts from the last 24 hours in the soccerbanners subreddit."""
    subreddit = reddit.subreddit('soccerbanners')
    
    # Calculate the timestamp for 24 hours ago
    cutoff_time = datetime.datetime.now() - timedelta(days=1)
    
    # Ensure the 'images' directory exists
    os.makedirs("images", exist_ok=True)
    
    # List to store post data (for future PostgreSQL insertion)
    posts_data = []

    for post in subreddit.new(limit=None):

        post_time = post.created_utc
        posted_time = datetime.datetime.fromtimestamp(post_time)
        
        # Break the loop if we've reached posts older than 24 hours
        if posted_time < cutoff_time:
            break
        
        # Extract required data
        post_id = post.id
        title = post.title
        
        
        # Download and save the image
        file_path = os.path.join("images", f"{post_id}.jpg")
        download_image(post.url, file_path)
        
        # Store post data (for future PostgreSQL insertion)
        posts_data.append((post_id, title, posted_time))
        
        # Print post information
        print(f"Post ID: {post_id}")
        print(f"Title: {title}")
        print(f"Posted at: {posted_time}")
        print("------------------------")

    print(f"Processed {len(posts_data)} posts")
    # Here you would typically insert posts_data into PostgreSQL
    # But as requested, we'll skip that part for now

def daily_job():
    """Run the post processing job."""
    print("Starting daily job to process posts from the last 24 hours...")
    process_posts()
    print("Daily job completed.")

if __name__ == "__main__":
    # Schedule the job to run daily at 6:00 AM
    schedule.every().day.at("15:48").do(daily_job)
    
    print("Scheduler started. Waiting for 6:00 AM to run the daily job...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute