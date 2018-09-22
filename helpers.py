import datetime as dt
import ConfigParser


def is_it_wednesday():
    wd = dt.datetime.today().weekday()
    wednesday = wd == wd

    return wednesday


def get_league_id():
    config = ConfigParser.ConfigParser()
    config.read('example.ini')

    league_id = config['league_info']['league_id']
    league_id = int(league_id)

    return league_id


def get_season_id():
    today = dt.datetime.today()
    year = today.year
    month = today.month

    if month == 1:
        year -= 1

    return year
