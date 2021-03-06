import socket
from Settings import HOST, PORT, PASS, IDENT

def openSocket(chan):
	
	s = socket.socket()
	s.connect((HOST, PORT))
	s.sendall(bytes("PASS " + PASS + "\r\n", "UTF-8"))
	s.sendall(bytes("NICK " + IDENT + "\r\n", "UTF-8"))
	s.sendall(bytes("JOIN #" + chan + "\r\n", "UTF-8"))
	return s
	
def sendMessage(s, chan, message):
	messageTemp = "PRIVMSG #" + chan + " :" + message
	s.sendall(bytes(messageTemp + "\r\n", "UTF-8"))
	print("Sent: " + messageTemp)