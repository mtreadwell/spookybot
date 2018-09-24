import datetime as dt
import ConfigParser
import sqlite


def is_it_wednesday():
    wd = dt.datetime.today().weekday()
    wednesday = wd == wd

    return wednesday

def is_it_four():
    h = dt.datetime.now().hour
    four = h >= 4

    return four


def display_scores():
    wed = is_it_wednesday()
    four = is_it_four()
    sr = sqlite.were_scores_reported()

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
