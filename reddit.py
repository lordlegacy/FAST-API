import praw
import requests
import re
import time
import os
import schedule

reddit = praw.Reddit(
    client_id="-rh-LDZNOQ",
    client_secret="-go3glxVcOBPIQ028JVztM1A",
    user_agent="myredditapp by /u/yourusername",
)

seen_posts_id = []

def download_and_save_image(post, seen_posts_id):
    post_id = post.id

    if post_id in seen_posts_id:
        print(f"Skipping post (ID: {post_id}) - Already downloaded")
        return 

    seen_posts_id.append(post_id)
    url = post.url
    file_name = post.title + f" ({post.id})"
    file_name = re.sub(r'[^\w\-_\. ]', '_', file_name)  
    file_name = os.path.join("posts", file_name) + ".jpg" 

    print("File name:", file_name)
    print("Title:", post.title)
    print("ID:", post.id)
    print("URL:", post.url)

    r = requests.get(url)
    with open(file_name, "wb") as f:
        f.write(r.content)
        print(f"Downloaded image: {file_name}")

def get_posts():
    subreddit = reddit.subreddit('soccerbanners')
    new_posts = subreddit.new(limit=3)  # Remove the limit to retrieve all new posts
    for post in new_posts:
        if post.id not in seen_posts_id:
            download_and_save_image(post, seen_posts_id)

def job():
    print("Checking for new posts...")
    get_posts()

if __name__ == "__main__":
    if not os.path.exists("posts"):
        os.makedirs("posts")
    
    schedule.every().day.at("07:00").do(job)
    
    while True:
        schedule.run_pending()
        print("i will check again after 10 seconds")
        time.sleep(10)  # Check for scheduled tasks every 10 seconds