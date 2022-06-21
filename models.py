import string


class User:
    def __init__(self, email: string, name: string, own_leagues_id: list, espectator_leagues_id: list):
        self.email = email
        self.name = name
        self.own_leagues_id = own_leagues_id
        self.espectator_leagues_id = espectator_leagues_id
