import string, subprocess, random, re, threading, time, datetime, json
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom
from Commands import *
from threading import Thread
from Settings import IDENT


# Connect to IRC/Channel and start listening

def joinChannel(user, newjoin):
	print(user)
	Thread(target = chatBot, args=(user,newjoin)).start()


def chatBot(chan, newjoin):
	lasttip = datetime.datetime.now()
	s = openSocket(chan)
	joinRoom(s, chan, newjoin)
	readbuffer = ""
	close = False

	while close != True:
		lastping = datetime.datetime.now()
		readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		js = open('users.txt')
		users = json.load(js)
		js.close()
		
		# User Settings Go Here
		caps = users[chan][0]
		
		if lasttip < datetime.datetime.now()-datetime.timedelta(hours=1):
			lasttip = datetime.datetime.now()
			commandFROGTip(s, chan, caps)
			

		for line in temp:
			print(line)
			# reply to IRC PING's so we dont get disconnected
			if "PING" in line:
				s.sendall(bytes("PONG :tmi.twitch.tv\r\n", "UTF-8" ))
				lastping = datetime.datetime.now()
				break
			user = getUser(line)
			message = getMessage(line)
			print (user + " typed :" + message)
			#Listen for !frogtip command
			if re.search(r'^!frogtip', message, re.IGNORECASE):
				if lasttip < datetime.datetime.now()-datetime.timedelta(seconds=15):
					commandFROGTip(s, chan, caps)
					lasttip = datetime.datetime.now()
					break
			if re.search(r'^!join', message, re.IGNORECASE):
				print(chan)
				if chan == IDENT.lower():
					if user not in users:
						newjoin = True
						users[user] = [0]
						sendMessage(s, chan, "Joining " + user + "'s channel. If you would like FROGTips to hop off, type !leave in your channel while FROG is nearby.")
						joinChannel(user, newjoin)
						with open('users.txt', 'w') as file:
							file.write(json.dumps(users))
							file.close
					else:
						sendMessage(s, chan, "FROGTips is already in this channel. Please do not hog FROG")
					break
				else:
					sendMessage(s, chan, "To have FROGTips join your channel, say !join in the chat at https://twitch.tv/frogtips")
					break
				break
			if re.search(r'^!leave', message, re.IGNORECASE):
				if chan == user:
					sendMessage(s, chan, "Leaving " + user + "'s channel. D:")
					del users[user]
					print(users)
					with open('users.txt', 'w') as file:
						file.write(json.dumps(users))
						file.close
					close = True
				else:
					sendMessage(s, chan, "Hop off, you aren't the channel owner.")
				break
			if re.search (r'^!caps', message, re.IGNORECASE):
				if chan == IDENT.lower():
					sendMessage(s, chan, "Toggling CAPS in " + user +"'s channel.")
					print(users[user][0])
					if users[user][0] == 1:
						users[user][0] = 0
						with open('users.txt', 'w') as file:
							file.write(json.dumps(users))
							file.close
					else:
						users[user][0] = 1
						with open('users.txt', 'w') as file:
							file.write(json.dumps(users))
							file.close
					break
				break
		time.sleep(0.2)
		if lastping < datetime.datetime.now()-datetime.timedelta(minutes=7):
			chatBot(chan, newjoin)
			close = True
		pass
		
		
		
	
#Start Thread and connect to chat
js = open('users.txt')
users = json.load(js)
js.close()
for key in users:
	newjoin = False
	t = Thread(target = chatBot, args=(key, newjoin))
	t.start()	
