import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

DB_CONFIG = {
    "MYSQL": {
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "host": os.getenv("MYSQL_HOST"),
        "port": os.getenv("MYSQL_PORT"),
        "database": os.getenv("MYSQL_DB"),
    },
    "POSTGRESQL": {
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
        "database": os.getenv("POSTGRES_DB"),
    }
}

# SQLAlchemy에서 사용할 DB URL 자동 생성
def get_database_url(db_type: str):
    config = DB_CONFIG.get(db_type.upper())
    if not config:
        raise ValueError(f"지원되지 않는 데이터베이스 타입: {db_type}")

    if db_type.upper() == "MYSQL":
        return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    elif db_type.upper() == "POSTGRESQL":
        return f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

# MySQL과 PostgreSQL의 연결 URL 생성
MYSQL_DATABASE_URL = get_database_url("MYSQL")
POSTGRESQL_DATABASE_URL = get_database_url("POSTGRESQL")
