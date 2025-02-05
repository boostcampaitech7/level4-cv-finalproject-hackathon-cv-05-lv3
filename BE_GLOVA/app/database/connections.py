from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import MYSQL_DATABASE_URL, POSTGRESQL_DATABASE_URL

# MySQL 연결
mysql_engine = create_engine(MYSQL_DATABASE_URL)
MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

# PostgreSQL 연결
postgresql_engine = create_engine(POSTGRESQL_DATABASE_URL)
PostgreSQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgresql_engine)

try:
    with mysql_engine.connect() as connection:
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

try:
    with postgresql_engine.connect() as connection:
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")


# MySQL DB 세션 생성 함수
def get_mysql_db():
    db = MySQLSessionLocal()
    try:
        yield db
    finally:
        db.close()

# PostgreSQL DB 세션 생성 함수
def get_postgresql_db():
    db = PostgreSQLSessionLocal()
    try:
        yield db
    finally:
        db.close()
