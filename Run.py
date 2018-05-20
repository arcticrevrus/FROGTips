import string, subprocess, random, re, threading, time, datetime
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom
from Functions import *
from Commands import *
from threading import Thread
#from commands import *
# Connect to IRC/Channel and start listening

s = openSocket()
joinRoom(s)

readbuffer = ""
lastping = datetime.datetime.now()



def reconnect():
	while True:
		#Reconnect if no messages occur for over 6 minutes
		if lastping < datetime.datetime.now()-datetime.timedelta(minutes=6):
			joinRoom(s)
			
			
#Start Thread and connect to chat
if __name__ == "__main__":
	t1 = Thread(target = reconnect)
	t1.setDaemon(True)
	t1.start()
	while True:
		readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
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
				commandFROGTip(s)
				break
		pass