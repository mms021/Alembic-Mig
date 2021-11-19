from alembic.config import Config
from alembic import command
import psycopg2
import os 
#os.system("python3 -m  sql")
from sql import get_config_file , script_bd


dsn = get_config_file()
connect = psycopg2.connect(host=dsn[0][1], dbname='postgres', user=dsn[2][1], password=dsn[3][1], port=5432 )
connect.autocommit = True

cursor = connect.cursor()
cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dsn[1][1]}'")
exists = cursor.fetchone()
if not exists:
    cursor.execute(f'CREATE DATABASE {dsn[1][1]}')
    connect2 = psycopg2.connect(host=dsn[0][1], dbname=dsn[1][1], user=dsn[2][1], password=dsn[3][1], port=5432 )
    connect2.autocommit = True
    cursor2 = connect2.cursor()
    cursor2.execute("CREATE SCHEMA IF NOT EXISTS base")
    cursor2.execute("CREATE SCHEMA IF NOT EXISTS conf_lc")
    cursor2.execute("CREATE SCHEMA IF NOT EXISTS refbook")
    script_bd(cursor2 , '../Domain.Postgres.Core/Sql/tau_current.sql')
    
os.system("alembic revision --autogenerate ")
os.system("alembic upgrade head")




