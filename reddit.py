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
    post_to_pick = random.randint(1, 10)

    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    return submission.url
