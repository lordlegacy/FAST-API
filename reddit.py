import praw
import requests
import os
import schedule
import time
from datetime import timedelta
import datetime
import psycopg2

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
    subreddit = reddit.subreddit('soccerbanners')
    
    # Calculate the timestamp for 24 hours ago
    cutoff_time = datetime.datetime.now() - timedelta(days=1)
    
    # Ensure the 'images' directory exists
    os.makedirs("images", exist_ok=True)
    
    # List to store post data (for future PostgreSQL insertion)
    posts_data = []

    for post in subreddit.new(limit=5):

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

    # PostgreSQL connection parameters
    db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "wearelegion",
    "host": "localhost",
    "port": "5432"
    }


    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Insert data into PostgreSQL
    insert_query = """
    INSERT INTO reddit_posts (post_id, title, posted_time)
    VALUES (%s, %s, %s)
    ON CONFLICT (post_id) DO NOTHING;
    """
    
    for post_id, title, posted_time in posts_data:
        cur.execute(insert_query, (post_id, title, posted_time))

    # Commit the transaction and close the connection
    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted {len(posts_data)} posts into PostgreSQL")

def daily_job():
    print("Starting daily job to process posts from the last 24 hours...")
    process_posts()
    print("Daily job completed.")

if __name__ == "__main__":
    # Schedule the job to run daily at 6:00 AM
    schedule.every().day.at("11:27").do(daily_job)
    
    print("Scheduler started. Waiting for 6:00 AM to run the daily job...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute