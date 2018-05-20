from Socket import openSocket, sendMessage
from Functions import *
from Settings import *

def commandFROGTip(s):
	tip = frogTip()
	sendMessage(s, tip)