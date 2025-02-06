from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from .config import MYSQL_DATABASE_URL, POSTGRESQL_DATABASE_URL, update_db_status, get_db_status
from .models import MySQLBase, PostgreSQLBase  # 모델 가져오기

# MySQL 연결
mysql_engine = create_engine(MYSQL_DATABASE_URL)
MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

# PostgreSQL 연결
postgresql_engine = create_engine(POSTGRESQL_DATABASE_URL)
PostgreSQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgresql_engine)

def init_db():
    print("🔄 Initializing Database Tables...")

    mysql_inspector = inspect(mysql_engine)
    postgresql_inspector = inspect(postgresql_engine)

    mysql_existing_tables = mysql_inspector.get_table_names()
    postgresql_existing_tables = postgresql_inspector.get_table_names()

    mysql_before = set(mysql_existing_tables)
    postgresql_before = set(postgresql_existing_tables)

    MySQLBase.metadata.create_all(bind=mysql_engine)
    PostgreSQLBase.metadata.create_all(bind=postgresql_engine)

    mysql_after = set(inspect(mysql_engine).get_table_names())
    postgresql_after = set(inspect(postgresql_engine).get_table_names())

    mysql_new_tables = mysql_after - mysql_before
    postgresql_new_tables = postgresql_after - postgresql_before

    mysql_created = bool(mysql_new_tables)
    postgresql_created = bool(postgresql_new_tables)

    update_db_status(mysql_created, postgresql_created)  # 상태 업데이트

    if not mysql_new_tables and not postgresql_new_tables:
        print("✅ Database Tables Initialized! (No changes needed)")
    else:
        print("✅ Database Tables Initialized!")
        if mysql_new_tables:
            print(f"🆕 New MySQL Tables Created: {mysql_new_tables}")
        if postgresql_new_tables:
            print(f"🆕 New PostgreSQL Tables Created: {postgresql_new_tables}")

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
