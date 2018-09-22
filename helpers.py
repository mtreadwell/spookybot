import datetime as dt
import ConfigParser


def is_it_wednesday():
    wd = dt.datetime.today().weekday()
    wednesday = wd == wd

    return wednesday


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
