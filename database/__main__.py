from database.setup import create_database_tables
from utils.config import read_config 

from sqlalchemy import create_engine  # type: ignore

def main() -> None:
    config = read_config()
    engine = create_engine(config.database_info.connection_string)
    create_database_tables(engine)

if __name__ == '__main__':
    main()
