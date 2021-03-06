import espn
import helpers
import os
import re
from slackclient import SlackClient
import sqlite
import reddit

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
bot_id = None
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events, bot_id_):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id_:
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
    # if command.startswith('waterbet'):
    #     response = 'Mike has some work to do here'
    #
    #     slack_client.api_call(
    #         "chat.postMessage",
    #         channel=channel,
    #         text=response
    #     )

    if command.startswith('constitution'):
        response = 'In order to form a more perfect Union: https://spooky.life'

        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )

    subreddit_command = helpers.get_subreddit_command()
    if command.startswith(subreddit_command):
        subreddit = helpers.get_subreddit_name()
        image = reddit.get_subreddit_image(subreddit)[0]
        attachments = [{"title": "", "image_url": image}]

        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text='',
            attachments=attachments
        )


def periodic_command():
    """
        Executes bot command when a timing condition is met
    """
    league_id = helpers.get_league_id()
    season_id = helpers.get_season_id()
    week = espn.get_last_week(league_id, season_id)

    if helpers.display_scores(week):
        channel = '#general'

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
