import datetime as dt
import ConfigParser
import sqlite
import pandas as pd


def is_it_wednesday():
    wd = dt.datetime.today().weekday()
    wednesday = wd == 2

    return wednesday


def is_it_four():
    h = dt.datetime.now().hour
    four = h >= 4

    return four


def were_scores_reported(week):
    conn = sqlite.create_connection()
    df = pd.read_sql_query("select * from matchup_info", conn)
    conn.close()

    reported = len(df[df['week'] == week]) > 0

    return reported


def display_scores(week):
    wed = is_it_wednesday()
    four = is_it_four()
    sr = were_scores_reported(week)

    display = wed & four & ~sr

    return display


def get_league_id():
    config = ConfigParser.RawConfigParser()
    config.read('spookybot.config')

    league_id = config.getint('league_info', 'league_id')

    return league_id


def get_season_id():
    today = dt.datetime.today()
    year = today.year
    month = today.month

    if month == 1:
        year -= 1

    return year


def get_db_name():
    config = ConfigParser.RawConfigParser()
    config.read('spookybot.config')

    db_name = config.get('db_info', 'db_name')

    return db_name
