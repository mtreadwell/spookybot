import espn
import helpers
import os
import re
from slackclient import SlackClient
import sqlite

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events, starterbot_id_):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id_:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # This is where you start to implement more commands!
    if command.startswith('do'):
        response = 'Don\'t tell me what to do'

        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )


def periodic_command():
    """
        Executes bot command when a timing condition is met
    """
    if helpers.display_scores():
        channel = '#general'
        league_id = helpers.get_league_id()
        season_id = helpers.get_season_id()
        week = espn.get_last_week(league_id, season_id)

        scoreboard = espn.get_scoreboard(league_id, season_id, week)
        matchup_info = espn.get_matchup_info(scoreboard)

        sqlite.write_table(matchup_info, 'matchup_info')

        matchup_text = espn.get_matchup_text(matchup_info)

        def send_score(score):
            slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=score
            )

        [send_score(mi) for mi in matchup_text]
