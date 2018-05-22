# FROGTips

FROGTips is a twitch/IRC chat bot intended to deliver FROGTips to twitch chats via a !frogtip command.

# Dependencies

FROGTips relies on Python 3 and the requests package to make requests to the FROGTips v3 API. Take care not to let Python eat FROG.

# Usage

1. Replace the first line of users.txt with the channel you want your bot to run in, and update Settings.py with the apropriate values.
2. Run Run.py
3. FROGTips has the ability to join multiple channels. If a user wishes to have FROGTips join their channel as well, they should hop over to the channel specified in IDENT and type !join.
