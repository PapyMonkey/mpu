from dataIO import dataIO
import os

config_FILEPATH = os.getcwd() + '/rsc/config.json'

if dataIO.is_valid_json(config_FILEPATH):
    config = dataIO._read_json(config_FILEPATH)
else:
    config = {
		"access_token": os.environ["ACCESS_TOKEN"],
		"client_id": os.environ["CLIENT_ID"],
        "client_id_secret": os.environ["CLIENT_ID_SECRET"],
		"prefix": "!"
    }
