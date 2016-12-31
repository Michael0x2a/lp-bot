from datetime import datetime

import praw

from crawler.models import Submission
from utils.config import RedditInfo
from utils.custom_types import HtmlStr, MarkdownStr

def run(info: RedditInfo) -> None:
    # Read-only reddit instance
    reddit = praw.Reddit(client_id=info.client_id,
                         client_secret=info.client_secret,
                         user_agent=info.user_agent)

    for submission in reddit.subreddit('learnprogramming').stream.submissions():
        print(submission.title)
        print(submission.author)
        #print(submission.created_utc)
        print(datetime.utcfromtimestamp(submission.created_utc))
        #print(submission.fullname)
        #print(submission.selftext)
        #print(submission.selftext_html)
        print(submission.url)
        print()

        '''Submission(
                title=submission.title
                author=submission.author
                created_utc=datetime.utcfromtimestamp(submission.created_utc),
                fullname=submission.fullname,
                body_markdown=MarkdownStr(submission.selftext),
                body_html=HtmlStr(submission.selftext_html),
                url=submission.url)'''
