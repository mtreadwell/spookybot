# spookybot

## Bot Setup
```
apt-get update
apt-get install -y python
apt-get install -y python-pip
apt-get install -y nano
apt-get install -y git

#required python libraries
pip install slackclient
pip install requests
pip install pandas
```

## Slack Setup:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

`export SLACK_BOT_TOKEN='slack_bot_token'`

## Configure GIT
```
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git clone https://github.com/mtreadwell/spookybot
```

## Update League ID
`nano spookybot/spookybot.config`
