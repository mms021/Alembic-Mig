from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
import os , json
import psycopg2
#os.system("python3 -m  Models.models")
#os.system("python3 -m  sql")

from Models.models import  target_metadata_main
from sql import clean_bd , pload_plain_sql , Post_InitData_cont ,Pre_InitData_cont ,Pol_instal , get_config_file , include_name


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

dsn = get_config_file()
config.set_main_option('sqlalchemy.url', f'postgresql://{dsn[2][1]}:{dsn[3][1]}@{dsn[0][1]}:5432/{dsn[1][1]}')

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

"""Базовые Мета классы """
target_metadata = target_metadata_main

"""Настройки для таблицы с версиями"""
version_table = 'upp_migration'
# version_table_schema =

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata, 
            version_table = version_table, 
            include_schemas=True,
            include_name = include_name
        )

        command = context.get_context().opts['fn'].__name__
        
        with context.begin_transaction():
            #target_metadata.metadata.reflect(engine=engine)
            print("Database migration started")
            context.run_migrations()

        if command == 'upgrade':
            connect = psycopg2.connect(host=dsn[0][1], dbname=dsn[1][1], user=dsn[2][1], password=dsn[3][1], port=5432 )
            connect.autocommit = True
            cursor = connect.cursor()
            clean_bd(cursor)
            print('Запускаем создание функций БД')
            pload_plain_sql(cursor)
            print('Загружаем системные справочники')
            Pre_InitData_cont(cursor)
            print('Загружаем данные необходимые для создания групповых политик')
            Pol_instal(cursor)
            print('Загружаем данные ядра')
            Post_InitData_cont(cursor)
            print('Migrate completed!')

            


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
