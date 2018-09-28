import requests as rq
import pandas as pd
import helpers


def get_scoreboard(league_id, season_id, week):
    sb = rq.get('http://games.espn.com/ffl/api/v2/scoreboard',
                params={'leagueId': league_id,
                        'seasonId': season_id,
                        'matchupPeriodId': week})

    sb = sb.json()

    return sb


def get_last_week(league_id, season_id):
    sb = rq.get('http://games.espn.com/ffl/api/v2/scoreboard',
                params={'leagueId': league_id,
                        'seasonId': season_id})

    sb = sb.json()

    week = sb['scoreboard']['scoringPeriodId']
    last_week = week - 1

    return last_week


def get_matchups(scoreboard):
    matchups = scoreboard['scoreboard']['matchups']

    return matchups


def get_win_loss(matchup):
    teams = matchup['teams']
    win = matchup['winner'] == 'home'

    winner = [i for i in teams if i['home'] == win][0]
    loser = [i for i in teams if i['home'] != win][0]

    wl_dict = {'winner': winner, 'loser': loser}

    return wl_dict


def get_team_name(team):
    team = team['team']
    location = team['teamLocation']
    nickname = team['teamNickname']
    team_name = location + ' ' + nickname

    return team_name


def get_team_score(team):
    score = team['score']

    return score


def get_matchup_info(scoreboard):
    matchups = get_matchups(scoreboard)
    win_loss = [get_win_loss(m) for m in matchups]

    def get_win_loss_info(win_loss_, result):
        info = [wl[result] for wl in win_loss_]
        name_list = [get_team_name(i) for i in info]
        score_list = [get_team_score(i) for i in info]

        result_dict = {result + '_name': name_list,
                       result + '_score': score_list}

        return result_dict

    winners = get_win_loss_info(win_loss, 'winner')
    losers = get_win_loss_info(win_loss, 'loser')

    def merge_two_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z

    matchup_info = merge_two_dicts(winners, losers)
    matchup_info = pd.DataFrame(matchup_info)

    league_id = helpers.get_league_id()
    season_id = helpers.get_season_id()
    week = get_last_week(league_id, season_id)

    matchup_info = matchup_info.assign(week=week)

    columns = ['week',
               'winner_name', 'loser_name',
               'winner_score', 'loser_score']
    matchup_info = matchup_info[columns]

    return matchup_info


def get_matchup_text(matchup_info):
    wn = list(matchup_info['winner_name'])
    ws = list(matchup_info['winner_score'])

    ln = list(matchup_info['loser_name'])
    ls = list(matchup_info['loser_score'])

    defeat_text = ['\n*{}* defeated *{}*'.format(w, l) for w, l in zip(wn, ln)]
    score_text = [' with a score of {} to {}\n'.format(w, l) for w, l in zip(ws, ls)]
    matchup_text = [d + s for d, s in zip(defeat_text, score_text)]

    return matchup_text
