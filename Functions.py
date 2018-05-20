import random, requests
from requests.auth import HTTPBasicAuth
from Socket import openSocket, sendMessage
from Settings import *

def frogTip():
	#replace UUID and passphrase with proper values
	r = requests.get('https://tadpole.frog.tips/api/3/tips', auth=HTTPBasicAuth('UUID', 'passphrase'))
	return random.choice(r.json())['tip']