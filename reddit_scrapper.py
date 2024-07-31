import praw
from datetime import datetime, timedelta
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, SUBREDDIT_NAME, POST_LIMIT

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        self.subreddit = self.reddit.subreddit(SUBREDDIT_NAME)

    def get_recent_posts(self):
        posts_data = []
        for post in self.subreddit.new(limit=POST_LIMIT):
            post_time = datetime.fromtimestamp(post.created_utc)
            posts_data.append({
                'post_id': post.id,
                'title': post.title,
                'url': post.url,
                'posted_time': post_time
            })
        return posts_data