from decouple import config

class ConfigLoader:
    def __init__(self):
        self.access_token = str(config('ACCESS_TOKEN'))
        self.client_id = str(config('CLIENT_ID'))
        self.client_id_secret = str(config('CLIENT_ID_SECRET'))
        self.prefix = '.'

    def get_access_token(self):
        return self.access_token

    def get_client_id(self):
        return self.client_id

    def get_client_id_secret(self):
        return self.client_id_secret

    def get_prefix(self):
        return self.prefix
