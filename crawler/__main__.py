import time

from threading import Thread
import crawler.extracter as extracter
from utils.config import read_config

def main() -> None:
    config = read_config()

    extracter_args = (config.reddit_info, config.database_info)

    submission_thread = Thread(
            target=extracter.extract_submissions,
            args=extracter_args,
            daemon=True)
    comment_thread = Thread(
            target=extracter.extract_comments,
            args=extracter_args,
            daemon=True)

    submission_thread.start()
    comment_thread.start()

    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()

