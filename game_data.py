'''
game_data.py

define the data structure for game data objects

generate saved file

'''

import shelve

class GameData:
    games = []

    def __init__(self, mode_id):
        cls.games.append(mode_id)
        
        self.max_time = None
        self.music = None
        self.n_actions = None
        self.targets = []


'''
Docs for actions

./media/actions/

*.jpg

1   arms up
2   arms down
3   arms high
4

6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26

'''