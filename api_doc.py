
## UI Module

## CONTROL -- game
'''
Run one game with given mode and id, return if the score, and grade.

Inputs:
    mode: 0 for pass mode, 1 for training mode  
    id: level number, to be appointed later
Outputs:
    score: num negative score of this round of game. 
    grade: "S", "A", "B", "C"; "F" for fail (in pass mode)
'''


def game_controller(mode: int, id: int) -> Tuple[int, str]: 
    ...
    return score, grade

