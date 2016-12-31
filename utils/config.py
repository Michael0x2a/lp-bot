from pathlib import Path
import json

from utils.custom_types import JsonDict
from utils.boundary import check_is_str, check_is_json_dict

DEFAULT_CONFIG = Path('lpbot_config.secret.json')

class DatabaseInfo:
    def __init__(self,
            connection_string: str) -> None:
        self.connection_string = connection_string

    @staticmethod
    def make(blob: JsonDict) -> 'DatabaseInfo':
        return DatabaseInfo(
                connection_string=check_is_str(blob['connection_string']))

class RedditInfo:
    def __init__(self,
            client_id: str,
            client_secret: str,
            user_agent: str,
            username: str,
            password: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
        self.password = password

    @staticmethod
    def make(blob: JsonDict) -> 'RedditInfo':
        return RedditInfo(
                client_id=check_is_str(blob['client_id']),
                client_secret=check_is_str(blob['client_secret']),
                user_agent=check_is_str(blob['user_agent']),
                username=check_is_str(blob['username']),
                password=check_is_str(blob['password']))

class Config:
    def __init__(self,
            reddit_info: RedditInfo,
            database_info: DatabaseInfo) -> None:
        self.reddit_info = reddit_info
        self.database_info = database_info

    @staticmethod
    def make(blob: JsonDict) -> 'Config':
        return Config(
                RedditInfo.make(check_is_json_dict(blob['reddit_info'])),
                DatabaseInfo.make(check_is_json_dict(blob['database_info'])))

def read_config(path: Path = DEFAULT_CONFIG) -> Config:
    with path.open() as stream:
        return Config.make(json.load(stream))

