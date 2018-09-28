import sqlite3 as sq
from sqlite3 import Error
import helpers


def create_connection():
    db = helpers.get_db_name()

    conn = sq.connect(db)
    return conn


def write_table(df, table):
    conn = create_connection()
    df.to_sql(table, conn, if_exists='append', index=False)
    conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def instantiate_db():
    bets = """CREATE TABLE IF NOT EXISTS bet_info (
                  id integer PRIMARY KEY,
                  date text NOT NULL,
                  party_first text NOT NULL,
                  party_second text NOT NULL,
                  desc text NOT NULL
                );"""

    matchups = """CREATE TABLE IF NOT EXISTS matchup_info (
                      id integer PRIMARY KEY,
                      week integer NOT NULL,
                      winner_name text NOT NULL,
                      loser_name text NOT NULL,
                      winner_score float NOT NULL,
                      loser_score float NOT NULL
                    );"""

    conn = create_connection()
    create_table(conn, bets)
    create_table(conn, matchups)

    conn.close()
