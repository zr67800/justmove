
## UI Module
'''
main_UI.py

UI module is implemented with tkinter

It controls the navigation inside the app

It calls other modules when needed

'''
class JustMove(tk.Tk):
    ...

if __name__ == '__main__':
    app = JustMove()
    app.mainloop()



## CONTROL -- game
'''
game_controller.py

Run one game with given mode and id, return if the score, and grade. 
It may call other control tools to finish the task.

Inputs:
    mode: 0 for pass mode, 1 for training mode  
    id: level number, to be appointed later
Outputs:
    score: num negative score of this round of game. 
    grade: "A", "B", "C"; "F" for fail (in pass mode)
'''


def game(mode: int, id: int) -> Tuple[int, str]: 
    ...
    return score, grade

## CONTROL -- posture recognition, grading, etc.
'''
To further break down the game controller. Not designed. Need experiment.
'''


## Data -- userdata
'''
userdata.py

Keeping a set of user data for each user, which includes username, password, progress, etc.
Handling sign up and log in.

'''




## Data -- leaderboard
'''
leaderboard.py

Maintaining a leaderboard
'''
class Leaderboard:
    def __init__(self, saved):
        ...

    def add(self, username, score):
        ...
    
    def get(self)
        ...
        return [(username, score), ...]



## Data -- gamedata
'''
gamedata.py

Feeding the game controller with level specific data such as targets and passing score.
'''

