from datetime import datetime
from utils.custom_types import MarkdownStr, HtmlStr

class Submission:
    def __init__(self,
                 title: str,
                 author: str,
                 created_utc: datetime,
                 fullname: str,
                 body_markdown: MarkdownStr,
                 body_html: HtmlStr,
                 url: str) -> None:
        self.title = title
        self.author = author
        self.created_utc = created_utc
        self.fullname = fullname
        self.body_markdown = body_markdown
        self.body_html = body_html
        self.url = url

