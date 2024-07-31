#database_handler
import psycopg2
from config import DB_PARAMS

class DatabaseHandler:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_PARAMS)
        self.cur = self.conn.cursor()

    def insert_posts(self, posts_data):
        insert_query = """
        INSERT INTO reddit_posts (post_id, title, posted_time)
        VALUES (%s, %s, %s)
        ON CONFLICT (post_id) DO NOTHING;
        """
        for post in posts_data:
            self.cur.execute(insert_query, (post['post_id'], post['title'], post['posted_time']))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()