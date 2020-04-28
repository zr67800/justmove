'''
JUST MOVE -- an fitness game app prototype with camera based human posture recognition.


This is the entry point of the game. To run the game, use Python 3.8+ with opencv. 
    python main_UI.py

This file includes the main part of the UI control and navigation.

'''


import tkinter as tk
import tkinter.font as tkFont

####==== dummy component ====####

#from game_controller import GameController
import time
class GameController:

    def game(mode, id):
        print (f"mode = {mode}, id = {id}")
        for i in range(5,0, -1):
            print(i)
            time.sleep(1)
        return 100, "A"


#from userdata import UserManager
class UserManager:
    def login(username, password):
        return True


####==== Meta parameters ====####

# This is for desktop
WINDOW_SIZE = (1280, 720)

# failing grades
FAIL = {"F"}


####==== Classes ====####

class JustMove(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkFont.Font(family = "Helvetica", size = 80)
        self.label_font = tkFont.Font(family = "Helvetica", size = 30)
        self.button_font = tkFont.Font(family = "Helvetica", size = 30)
        self.small_button_font = tkFont.Font(family = "Helvetica", size = 15)

        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.title("Just Move")

        self.main_window = tk.Frame(self, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main_window.pack(side="top", fill="both", expand=True)

        self.pages = dict()
        for F in {
                    BlankPage,          # id = 0   
                    WelcomePage,        # id = 1
                    LoginPage,          # id = 2
                    SignUpPage,         # id = 3
                    PassModePage,       # id = 4
                    TrainingModePage,   # id = 5
                    RankPage,           # id = 6
                    MyPage,             # id = 7
                    LevelSelectionPage, # id = 8
                    ResultPage,         # id = 9



                  }:
            page_id = F.id 
            frame = F(self.main_window, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[page_id] = frame

        self.current_result = None




        self.show_page(WelcomePage.id)

    def show_page(self, page_id):
        frame = self.pages[page_id]
        frame.tkraise()
        frame.event_generate("<<OnRaise>>")

    def set_score_and_grade(self, score, grade):
        self.current_result = (score, grade) 

    def get_score_and_grade(self):
        assert (self.current_result is not None)
        return self.current_result



class WelcomePage(tk.Frame):
    id = 1

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        

        self.label = tk.Label(self, text = "Just Move", font = main.title_font)
        self.label.pack()

        self.small_label = tk.Label(self, text = "keep fit with fun", font = main.label_font)
        self.small_label.pack()

        self.start_button = tk.Button(self, text = "Start", command = lambda : main.show_page(LoginPage.id), font = main.button_font)
        self.start_button.pack()

        self.exit_button = tk.Button(self, text = "Exit" , command = main.quit, font = main.button_font)
        self.exit_button.pack()

class LoginPage(tk.Frame):
    id = 2

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.label = tk.Label(self, text = "please log in", font = main.label_font)
        self.label.pack()

        #TODO later: clear default value in Entry at mouse clicks

        self.username = tk.Entry(self,textvariable = tk.StringVar(self, value = "username"), font = main.label_font)
        self.username.pack()

        self.password = tk.Entry(self,textvariable = tk.StringVar(self, value = "password"), font = main.label_font)
        self.password.pack()

        #small_label = tk.Label(self, text = "keep fit with fun")
        self.login_button = tk.Button(self, text = "Login", command = self.login, font = main.button_font)
        self.login_button.pack()

        self.back_button = tk.Button(self, text = "Cancel" , command = lambda : main.show_page(WelcomePage.id), font = main.button_font)
        self.back_button.pack()

        self.signup_button = tk.Button(self, text = "Sign up" , command = lambda : main.show_page(SignUpPage.id), font = main.small_button_font)
        self.signup_button.pack()

    def login(self):
        username_ = self.username.get()
        password_ = self.password.get()
        print(f"Login: {username_}, {password_}")
        allowed = UserManager.login(username = username_, password = password_)
        if allowed:
            self.main.show_page(PassModePage.id)
        else:
            # TODO: handel wrong password/non existing username
            pass

class SignUpPage(tk.Frame):
    id = 3

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.back_button = tk.Button(self, text = "back" , command = lambda : main.show_page(LoginPage.id), font = main.button_font)
        self.back_button.grid(row=0,column=0,sticky="NW")
        # TODO

class PassModePage(tk.Frame):
    id = 4

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.label = tk.Label(self, text = "Pass Mode", font = main.label_font)
        self.label.pack()

        self.start_button = tk.Button(self, text = "Start" , command = lambda : main.show_page(LevelSelectionPage.id), font = main.button_font)
        self.start_button.pack()

        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id), state=tk.DISABLED)
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id))
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id))
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id))
        self.pass_mode_button.pack()
        self.training_mode_button.pack()
        self.rank_button.pack()
        self.my_button.pack()
        # TODO

class TrainingModePage(tk.Frame):
    id = 5

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.label = tk.Label(self, text = "Training Mode", font = main.label_font)
        self.label.pack()


        # TODO

        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id))
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id), state=tk.DISABLED)
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id))
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id))
        self.pass_mode_button.pack()
        self.training_mode_button.pack()
        self.rank_button.pack()
        self.my_button.pack()

class RankPage(tk.Frame):
    id = 6

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.label = tk.Label(self, text = "Rank", font = main.label_font)
        self.label.pack()

        # TODO

        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id))
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id))
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id), state=tk.DISABLED)
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id))
        self.pass_mode_button.pack()
        self.training_mode_button.pack()
        self.rank_button.pack()
        self.my_button.pack()

class MyPage(tk.Frame):
    id = 7

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.label = tk.Label(self, text = "My infomation", font = main.label_font)
        self.label.pack()

        self.logout_button = tk.Button(self, text = "Log out" , command = lambda : main.show_page(LoginPage.id), font = main.button_font)
        self.logout_button.pack()
        # TODO

        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id))
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id))
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id))
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id), state=tk.DISABLED)
        self.pass_mode_button.pack()
        self.training_mode_button.pack()
        self.rank_button.pack()
        self.my_button.pack()

class LevelSelectionPage(tk.Frame):
    id = 8

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.back_button = tk.Button(self, text = "back" , command = lambda : main.show_page(PassModePage.id))
        self.back_button.pack()

        self.label = tk.Label(self, text = "Pass Mode", font = main.label_font)
        self.label.pack()

        self.levels = [
            tk.Button(self, text = "Level 1", command = lambda : self.level(1)),
            tk.Button(self, text = "Level 2", command = lambda : self.level(2)),
            tk.Button(self, text = "Level 3", command = lambda : self.level(3)),
            tk.Button(self, text = "Level 4", command = lambda : self.level(4)),
            tk.Button(self, text = "Level 5", command = lambda : self.level(5)),
        ]
        for l in self.levels:
            l.pack()

        # TODO

    def level(self, level_id):
        self.main.show_page(BlankPage.id)
        mode = 0 # pass mode
        score, grade = GameController.game(mode, level_id)
        print(score, grade)
        self.main.set_score_and_grade(score, grade)
        self.main.show_page(ResultPage.id)

class ResultPage(tk.Frame):
    id = 9

    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.bind("<<OnRaise>>", self.on_raise)

        self.grade = tk.StringVar()
        self.score = tk.StringVar()
        self.msg = tk.StringVar()

        self.grade_label = tk.Label(self, textvariable = self.grade, font = main.title_font)
        self.score_label = tk.Label(self, textvariable = self.score, font = main.label_font)
        self.msg_label = tk.Label(self, textvariable = self.msg, font = main.label_font)

        self.grade_label.pack()
        self.score_label.pack()
        self.msg_label.pack()


        self.pass_msg = "Congratulations!\nYou did a great job to unlock the next level!"
        self.fail_msg = "Try again, you can do better"

        self.cont_button = tk.Button(self, text = "OK", command = lambda : main.show_page(LevelSelectionPage.id), font = main.button_font)
        self.cont_button.pack()

    def on_raise(self, event):
        score, grade = self.main.get_score_and_grade()
        self.grade.set(grade)
        self.score.set(score)
        if grade in FAIL:
            self.msg.set(self.fail_msg)
        else:
            self.msg.set(self.pass_msg)
            # TODO: deal with leaderboard and progress (or should this be done within GameController?)
        





class BlankPage(tk.Frame):
    id = 0
    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
    
####==== Main ====####

if __name__ == '__main__':
    app = JustMove()
    app.mainloop()

