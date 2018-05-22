import os, random, time, requests, random
from requests.auth import HTTPBasicAuth
from Socket import openSocket, sendMessage
from Settings import *

def commandFROGTip(s, chan):
	r = requests.get('https://tadpole.frog.tips/api/3/tips', auth=HTTPBasicAuth(UUID, PASSPHRASE))
	tip=random.choice(r.json())['tip']
	sendMessage(s, chan, tip)