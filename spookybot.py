import slack
import time
import sqlite

RTM_READ_DELAY = 1

if __name__ == "__main__":
    sqlite.instantiate_db()

    if slack.slack_client.rtm_connect(with_team_state=False):
        print("Spookybot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack.slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = slack.parse_bot_commands(
                slack.slack_client.rtm_read(),
                bot_id
            )
            if command:
                slack.handle_command(command, channel)

            slack.periodic_command()
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
