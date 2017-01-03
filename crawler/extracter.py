from typing import Any, TypeVar, List, Callable, Type, Union
from datetime import datetime
import time

import praw  # type: ignore

from database.schema import Submission, Comment
from database.abstraction import Database

from utils.config import SubredditInfo, RedditInfo, DatabaseInfo
from utils.custom_types import HtmlStr, MarkdownStr
from crawler.stream import stream_items


def extract_info(subreddit_info: SubredditInfo,
                 reddit_info: RedditInfo,
                 db_info: DatabaseInfo) -> None:
    # Read-only reddit instance
    reddit = praw.Reddit(client_id=reddit_info.client_id,
                         client_secret=reddit_info.client_secret,
                         user_agent=reddit_info.user_agent,
                         username=reddit_info.username,
                         password=reddit_info.password)

    # Database abstraction
    db = Database(db_info)

    # Setup data streams
    subreddit = reddit.subreddit(subreddit_info.name)
    submissions_stream = stream_items(subreddit.new)
    comments_stream = stream_items(subreddit.comments)

    # Handle initial (which could contain old data)
    extract_initial(db, next(submissions_stream), parse_raw_submission, Submission)
    extract_initial(db, next(comments_stream), parse_raw_comment, Comment)

    # Insert all new data
    while True:
        extract_new(db, next(submissions_stream), parse_raw_submission)
        extract_new(db, next(comments_stream), parse_raw_comment)
        time.sleep(3)



T = TypeVar('T', Submission, Comment)
def extract_initial(db: Database,
                    initial: List[Any],
                    parser: Callable[[Any], T],
                    table: Type[T]) -> None:
    with db.commit_only_session() as session:
        out = []
        for item in initial:
            model = parser(item)
            count = (session.query(table)
                     .filter(table.fullname == model.fullname)
                     .count())

            if count == 0:
                out.append(model)
                model.debug()
        session.add_all(out)

def extract_new(db: Database,
                data: List[Any],
                parser: Callable[[Any], Union[Submission, Comment]]) -> None:
    with db.commit_only_session() as session:
        models = [parser(item) for item in data]
        for model in models:
            model.debug()
        session.add_all(models)


def parse_raw_submission(submission: Any) -> Submission:
    return Submission(
            title=submission.title,
            author=submission.author.name,
            created_utc=datetime.utcfromtimestamp(submission.created_utc),
            fullname=submission.fullname,
            body_markdown=MarkdownStr(submission.selftext),
            body_html=HtmlStr(submission.selftext_html),
            url=submission.url)

def parse_raw_comment(comment: Any) -> Submission:
    return Comment(
            author=comment.author.name,
            created_utc=datetime.utcfromtimestamp(comment.created_utc),
            fullname=comment.fullname,
            body_markdown=MarkdownStr(comment.body),
            body_html=HtmlStr(comment.body_html),
            url=comment.link_url,
            parent=comment.parent_id)

'''
def extract_submissions(reddit_info: RedditInfo, db_info: DatabaseInfo) -> None:
    # Read-only reddit instance
    reddit = praw.Reddit(client_id=reddit_info.client_id,
                         client_secret=reddit_info.client_secret,
                         user_agent=reddit_info.user_agent,
                         username=reddit_info.username,
                         password=reddit_info.password)

    # Database abstraction
    db = Database(db_info)
    
    initial = True
    for submissions in stream_items(reddit.subreddit('lptest').new):
        with db.commit_only_session() as session:
            out = []
            for submission in submissions:
                model = Submission(
                        title=submission.title,
                        author=submission.author.name,
                        created_utc=datetime.utcfromtimestamp(submission.created_utc),
                        fullname=submission.fullname,
                        body_markdown=MarkdownStr(submission.selftext),
                        body_html=HtmlStr(submission.selftext_html),
                        url=submission.url)
                
                if initial:
                    count = (session.query(Submission)
                             .filter(Submission.fullname == model.fullname)
                             .count())
                    if count != 0:
                        continue

                out.append(model)

                print('Submission')
                print(model.title)
                print(model.author)
                print(model.created_utc)
                print()

                session.add(model)
            initial = True
        
def extract_comments(reddit_info: RedditInfo, db_info: DatabaseInfo) -> None:
    # Read-only reddit instance
    reddit = praw.Reddit(client_id=reddit_info.client_id,
                         client_secret=reddit_info.client_secret,
                         user_agent=reddit_info.user_agent,
                         username=reddit_info.username,
                         password=reddit_info.password)

    # Database abstraction
    db = Database(db_info)

    for comment in stream_items(reddit.subreddit('lptest').comments):
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
'''
