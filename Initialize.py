import string
from Socket import sendMessage
def joinRoom(s, chan, newjoin):
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	if newjoin == True:
		sendMessage(s, chan, "Successfully joined chat, type !frogtip to recieve FROG tips. If you would like FROGTips to hop off, type !leave in your channel while FROG is nearby.")
	
def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True