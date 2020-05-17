'''
game_data.py

define the data structure for game data objects

generate saved file

'''

import shelve

class GameDataLoader:
    def __init__(self, mode, id):
        # dummy things for testing 
        self.music = './media/music/1_0.mp3'
        #self.n_actions = 12
        self.max_time = 30
        self.actions = [(10,1,0,1), #(start_time, duration, is_persistent, action id)
                        (11,1,0,2),
                        (12,1,0,1),
                        (13,1,0,2),
                        (14,1,0,1),
                        (15,1,0,2),
                        (16,1,0,1),
                        (17,1,0,2),
                        (18,1,0,1),
                        (19,1,0,2),
                        (20,4,1,3),
                        (26,4,1,3),
                        ]
        self.target_dict = {1:((109, 32),(109, 75),(80, 86),(29, 96),(36, 53),(138, 96),(190, 107),(190, 64),(95, 182),(87, 258),(87, 333),(124, 182),(131, 258),(131, 333),(109, 139)),
                            2:((102, 10),(109, 61),(81, 71),(27, 71),(40, 102),(136, 71),(183, 71),(177, 92),(88, 164),(81, 246),(81, 317),(122, 164),(129, 246),(129, 317),(109, 123)),
                            3:((90, 89),(95, 153),(112, 166),(50, 102),(56, 51),(73, 153),(135, 102),(140, 64),(78, 256),(84, 397),None,(101, 256),(112, 397),None,(90, 205)),

                            }



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