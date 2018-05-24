import os, random, time, requests, random
from requests.auth import HTTPBasicAuth
from Socket import openSocket, sendMessage
from Settings import *

def upper_repl(match):
	return match.group(0).upper()
	
def commandFROGTip(s, chan, caps):
	r = requests.get('https://tadpole.frog.tips/api/3/tips', auth=HTTPBasicAuth(UUID, PASSPHRASE))
	tip=random.choice(r.json())['tip']
	if caps == True:
		tip=tip.lower()
		tip = re.sub(r'frog', upper_repl, tip)
		sendMessage(s, chan, tip)
	else:
		sendMessage(s, chan, tip)