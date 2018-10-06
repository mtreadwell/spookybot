import praw
import random
import os


def reddit_connection():
    reddit_client_id = os.environ.get('REDDIT_CLIENT_ID')
    reddit_client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
    reddit_user_agent = os.environ.get('REDDIT_USER_AGENT')

    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         user_agent=reddit_user_agent)

    return reddit


def get_subreddit_image(subreddit):
    reddit = reddit_connection()

    memes_submissions = reddit.subreddit(subreddit).hot()
    submissions = [x.url for x in memes_submissions if not x.stickied]

    submissions = [x for x in submissions if "comments" not in x]
    submissions = [x for x in submissions if "gif" not in x]
    submissions = [x for x in submissions if "gfy" not in x]
    submissions = [x for x in submissions if "video" not in x]

    submission = random.sample(submissions, 1)

    return submission
