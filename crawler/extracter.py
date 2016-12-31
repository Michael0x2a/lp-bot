from datetime import datetime

import praw  # type: ignore

from database.schema import Submission, Comment
from database.abstraction import Database

from utils.config import RedditInfo, DatabaseInfo
from utils.custom_types import HtmlStr, MarkdownStr

def extract_submissions(reddit_info: RedditInfo, db_info: DatabaseInfo) -> None:
    # Read-only reddit instance
    reddit = praw.Reddit(client_id=reddit_info.client_id,
                         client_secret=reddit_info.client_secret,
                         user_agent=reddit_info.user_agent,
                         username=reddit_info.username,
                         password=reddit_info.password)

    # Database abstraction
    db = Database(db_info)

    for submission in reddit.subreddit('lptest').stream.submissions():
        with db.commit_only_session() as session:
            model = Submission(
                    title=submission.title,
                    author=submission.author.name,
                    created_utc=datetime.utcfromtimestamp(submission.created_utc),
                    fullname=submission.fullname,
                    body_markdown=MarkdownStr(submission.selftext),
                    body_html=HtmlStr(submission.selftext_html),
                    url=submission.url)
            
            count = (session.query(Submission)
                     .filter(Submission.fullname == model.fullname)
                     .count())

            if count == 0:
                print('Submission')
                print(model.title)
                print(model.author)
                print(model.created_utc)
                print()

                session.add(model)
        
def extract_comments(reddit_info: RedditInfo, db_info: DatabaseInfo) -> None:
    # Read-only reddit instance
    reddit = praw.Reddit(client_id=reddit_info.client_id,
                         client_secret=reddit_info.client_secret,
                         user_agent=reddit_info.user_agent,
                         username=reddit_info.username,
                         password=reddit_info.password)

    # Database abstraction
    db = Database(db_info)

    for comment in reddit.subreddit('lptest').stream.comments():
        with db.commit_only_session() as session:
            model = Comment(
                    author=comment.author.name,
                    created_utc=datetime.utcfromtimestamp(comment.created_utc),
                    fullname=comment.fullname,
                    body_markdown=MarkdownStr(comment.body),
                    body_html=HtmlStr(comment.body_html),
                    url=comment.link_url,
                    parent=comment.parent_id)
            
            count = (session.query(Comment)
                     .filter(Submission.fullname == model.fullname)
                     .count())

            if count == 0:
                print('Comment')
                print(model.author)
                print(model.created_utc)
                print(model.url)
                print()

                session.add(model)

