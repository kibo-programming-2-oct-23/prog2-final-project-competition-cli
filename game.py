import json
from datetime import datetime, timedelta

# Make this serialized already. This is the example they can 
# redo this for the tournament class

class Game:
    def __init__(self, game_name, start_time, end_time, player_1 = 'Unknown', player_2 = 'Unknown'):
        self.name = game_name
        self.start_time = start_time
        self.end_time = end_time
        self.player_1 = player_1
        self.player_2 = player_2

    def description(self):
        return f'{self.name} at {str(self.start_time)}: {self.player_1} VS {self.player_2}'

    def __repr__(self):
        return self.description()

    # Milestone 3
    def update(self, player_1, player_2):
        pass

    def to_json_string(self):
        return json.dumps({'game_name': self.name, 'player_1': self.player_1, 'player_2': self.player_2, 'start_time': self.start_time, 'end_time': self.end_time })

    @staticmethod
    def from_json_string(input_string):
        game_dict = json.loads(input_string)
        return Game(game_dict.get('game_name'), game_dict.get('start_time'), game_dict.get('end_time'), game_dict.get('player_1'), game_dict.get('player_2'))
