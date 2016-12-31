import time
import crawler.extracter as extracter
from utils.config import read_config

def main() -> None:
    config = read_config()
    extracter.run(config.reddit_info)
    #while True:
    #    extracter.run(config.reddit_info)
    #    time.sleep(5)

if __name__ == '__main__':
    main()

