import string, subprocess, random, re, threading, time, datetime
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
		readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		if lasttip < datetime.datetime.now()-datetime.timedelta(hours=1):
			lasttip = datetime.datetime.now()
			commandFROGTip(s, chan)

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
					commandFROGTip(s, chan)
					lasttip = datetime.datetime.now()
					break
			if re.search(r'^!join', message, re.IGNORECASE):
				print(chan)
				if chan == IDENT.lower():
					if user not in users:
						newjoin = True
						users.append(user)
						sendMessage(s, chan, "Joining " + user + "'s channel. If you would like FROGTips to hop off, type !leave in your channel while FROG is nearby.")
						joinChannel(user, newjoin)
						with open ('users.txt', 'a') as f:
							f.write(user + "\n")
							f.close()
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
					f = open("users.txt", "r")
					lines = f.readlines()
					f.close()
					f = open("users.txt", "w")
					for line in lines:
						if line!=user + "\n":
							f.write(line)
					users.remove(user)
					close = True
				else:
					sendMessage(s, chan, "Hop off, you aren't the channel owner.")
				break
		time.sleep(0.2)
		pass
	
#Start Thread and connect to chat
with open ('users.txt') as f:
	users = f.read().splitlines()
for item in users:
	newjoin = False
	t = Thread(target = chatBot, args=(item, newjoin))
	t.start()	
while True:
	time.sleep(0.2)
	pass
