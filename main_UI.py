'''
JUST MOVE -- an fitness game app prototype with camera based human posture recognition.


This is the entry point of the game. To run the game, use Python 3.8+ with opencv. 
    python main_UI.py

This file includes the main part of the UI control and navigation.

'''
import os

import tkinter as tk
import tkinter.font as tkFont

import game_controller as GameController
from user_manager import UserManager
user = UserManager()


####==== Meta parameters ====####

# This is for desktop
WINDOW_SIZE = (1280, 720)

# failing grades
FAIL = {"F"}

# picture 
PIC = os.path.abspath("./media/pics/")
imgs = {}
img_names = {"title", "blank", "login", "my", "pass_mode", "rank", "result", "training"}


####==== Classes ====####

class JustMove(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # load pics
        for name in img_names:
            imgs[name] = tk.PhotoImage(file=PIC+f"/{name}.png")

        self.title_font = tkFont.Font(family = "Helvetica", size = 80)
        self.label_font = tkFont.Font(family = "Helvetica", size = 30)
        self.button_font = tkFont.Font(family = "Helvetica", size = 30)
        self.small_button_font = tkFont.Font(family = "Helvetica", size = 15)

        self.button_colour = "#C7DBDF"

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
    # DONE
    id = 1

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bg = tk.Label(self, image = imgs["title"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        

        self.start_button = tk.Button(self, text = "Start", command = lambda : main.show_page(LoginPage.id), font = main.button_font, highlightbackground = main.button_colour)
        self.start_button.place(x = X//2-60, y = Y//2+100, width = 120, height = 40)

        self.exit_button = tk.Button(self, text = "Exit" , command = main.quit, font = main.button_font, highlightbackground = main.button_colour)
        self.exit_button.place(x = X//2-60, y = Y//2+200, width = 120, height = 40 )

class LoginPage(tk.Frame):
    # DONE
    id = 2

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bg = tk.Label(self, image = imgs["login"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        
        self._clear_done = False

        self.username = tk.Entry(self,textvariable = tk.StringVar(self, value = "username"), font = main.label_font)
        self.username.bind("<1>", self._clear)
        self.username.place(x = X//2-200, y = Y//2-100, width = 400, height = 40)

        self.password = tk.Entry(self,textvariable = tk.StringVar(self, value = "password"), font = main.label_font)
        self.password.place(x = X//2-200, y = Y//2-20, width = 400, height = 40)

        #small_label = tk.Label(self, text = "keep fit with fun")
        self.login_button = tk.Button(self, text = "Login", command = self.login, font = main.button_font)
        self.login_button.place(x = X//2-160, y = Y//2+80, width = 120, height = 40)

        self.back_button = tk.Button(self, text = "Cancel" , command = lambda : main.show_page(WelcomePage.id), font = main.small_button_font)
        self.back_button.place(x = X//2-40, y = Y//2+160, width = 80, height = 25)

        self.signup_button = tk.Button(self, text = "Sign up" , command = lambda : main.show_page(SignUpPage.id), font = main.button_font)
        self.signup_button.place(x = X//2+40, y = Y//2+80, width = 120, height = 40)

    def _clear(self, event):
        if not self._clear_done:
            self.username.delete(0,tk.END)
            self.password.delete(0,tk.END)
            self.password["show"] = "*"
            self._clear_done = True


    def login(self):
        username_ = self.username.get()
        password_ = self.password.get()
        print(f"Login: {username_}, {password_}")
        allowed = user.login(username = username_, password = password_)
        if allowed:
            self.main.show_page(PassModePage.id)
        else:
            self._clear_done = False
            self._clear(None)

class SignUpPage(tk.Frame):
    # DONE
    id = 3

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bg = tk.Label(self, image = imgs["login"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        
        self._clear_done = False

        self.username = tk.Entry(self,textvariable = tk.StringVar(self, value = "username"), font = main.label_font)
        self.username.bind("<2>", self._clear)
        self.username.place(x = X//2-200, y = Y//2-100, width = 400, height = 40)

        self.password = tk.Entry(self,textvariable = tk.StringVar(self, value = "password"), font = main.label_font)
        self.password.place(x = X//2-200, y = Y//2-20, width = 400, height = 40)


        self.login_button = tk.Button(self, text = "Sign Up", command = self.signup, font = main.button_font)
        self.login_button.place(x = X//2-160, y = Y//2+80, width = 120, height = 40)

        self.back_button = tk.Button(self, text = "Cancel" , command = lambda : main.show_page(LoginPage.id), font = main.button_font)
        self.back_button.place(x = X//2+40, y = Y//2+80, width = 120, height = 40)



    def _clear(self, event):
        if not self._clear_done:
            self.username.delete(0,tk.END)
            self.password.delete(0,tk.END)
            self.password["show"] = "*"
            self._clear_done = True


    def signup(self):
        username_ = self.username.get()
        password_ = self.password.get()
        if len(username_)<3 or len(password_)<3:
            self._clear_done = False
            self._clear(None)
            return

        print(f"Sign up: {username_}, {password_}")
        allowed = user.signup(username = username_, password = password_)
        if allowed:
            self.main.show_page(LoginPage.id)
        else:
            self._clear_done = False
            self._clear(None)


class PassModePage(tk.Frame):
    # DONE
    id = 4

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bg = tk.Label(self, image = imgs["pass_mode"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_button = tk.Button(self, text = "Start" , command = lambda : main.show_page(LevelSelectionPage.id), font = main.button_font)
        self.start_button.place(x = X//2-80, y = Y//2, width = 160, height = 60)

        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id), state=tk.DISABLED, font = main.small_button_font)
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id), font = main.small_button_font)
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id), font = main.small_button_font)
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id), font = main.small_button_font)
        self.pass_mode_button.place(x = X//2-360, y = Y//2+250, width = 120, height = 25)
        self.training_mode_button.place(x = X//2-160, y = Y//2+250, width = 120, height = 25)
        self.rank_button.place(x = X//2+40, y = Y//2+250, width = 120, height = 25)
        self.my_button.place(x = X//2+240, y = Y//2+250, width = 120, height = 25)
        

class TrainingModePage(tk.Frame):
    # DONE
    id = 5

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bg = tk.Label(self, image = imgs["training"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.arm_button = tk.Button(self, text = ">>>" , command = lambda : self.training(1), font = main.small_button_font)
        self.arm_button.place(x = 885, y = 255, width = 40, height = 25)
        self.thigh_button = tk.Button(self, text = ">>>" , command = lambda : self.training(2), font = main.small_button_font)
        self.thigh_button.place(x = 870, y = 460, width = 40, height = 25)

        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id), font = main.small_button_font)
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id), state=tk.DISABLED, font = main.small_button_font)
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id), font = main.small_button_font)
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id), font = main.small_button_font)
        self.pass_mode_button.place(x = X//2-360, y = Y//2+250, width = 120, height = 25)
        self.training_mode_button.place(x = X//2-160, y = Y//2+250, width = 120, height = 25)
        self.rank_button.place(x = X//2+40, y = Y//2+250, width = 120, height = 25)
        self.my_button.place(x = X//2+240, y = Y//2+250, width = 120, height = 25)

    def training(self, id):
        # 1: arm, 2: thigh
        self.main.show_page(BlankPage.id)
        mode = 1 # training mode
        grade, score = GameController.game(mode, id)
        print(score, grade)
        user.add_score(score)
        self.main.set_score_and_grade(score, grade)
        self.main.show_page(ResultPage.id)
        
class RankPage(tk.Frame):
    # DONE
    id = 6

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bg = tk.Label(self, image = imgs["rank"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.bind("<<OnRaise>>", self.show_rank)

        self.a = dict()
        self.b = dict()
        self.c = dict()
        order = ("1st", "2nd", "3rd", "4th", "5th")
        for i in range(5):
            self.a[i] = tk.Label(self, text = order[i], font = main.small_button_font)
            self.b[i] = tk.Label(self, text = "-", font = main.small_button_font)
            self.c[i] = tk.Label(self, text = "0", font = main.small_button_font)
            
            self.a[i].place(x = X//2 - 220, y = Y//2 - 140 + i*60, width = 80, height = 25)
            self.b[i].place(x = X//2 - 40, y = Y//2 - 140 + i*60, width = 80, height = 25)
            self.c[i].place(x = X//2 + 140, y = Y//2 - 140 + i*60, width = 80, height = 25)


        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id), font = main.small_button_font)
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id), font = main.small_button_font)
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id), state=tk.DISABLED, font = main.small_button_font)
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id), font = main.small_button_font)
        self.pass_mode_button.place(x = X//2-360, y = Y//2+250, width = 120, height = 25)
        self.training_mode_button.place(x = X//2-160, y = Y//2+250, width = 120, height = 25)
        self.rank_button.place(x = X//2+40, y = Y//2+250, width = 120, height = 25)
        self.my_button.place(x = X//2+240, y = Y//2+250, width = 120, height = 25)

    def show_rank(self,event):
        ranks = user.get_leaderboard()
        print (ranks)
        for i in range (min(len(ranks), 5)):
            self.b[i]['text'] = ranks[i][0]
            self.c[i]['text'] = str(ranks[i][1])
            
        

class MyPage(tk.Frame):
    # DONE
    id = 7

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bind("<<OnRaise>>", self.get_info)

        self.bg = tk.Label(self, image = imgs["my"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.name1 = tk.Label(self, text = "Name: ", font = main.small_button_font)
        self.name2 = tk.Label(self, text = "-", font = main.small_button_font)
        self.name1.place(x = X//2 - 110, y = Y//2 - 160, width = 80, height = 25)
        self.name2.place(x = X//2 + 30, y = Y//2 - 160, width = 80, height = 25)

        self.score1 = tk.Label(self, text = "Score: ", font = main.small_button_font)
        self.score2 = tk.Label(self, text = "-", font = main.small_button_font)
        self.score1.place(x = X//2 - 110, y = Y//2 - 80, width = 80, height = 25)
        self.score2.place(x = X//2 + 30, y = Y//2 - 80, width = 80, height = 25)

        self.prog1 = tk.Label(self, text = "Progress: ", font = main.small_button_font)
        self.prog2 = tk.Label(self, text = "Level 0", font = main.small_button_font)
        self.prog1.place(x = X//2 - 110, y = Y//2, width = 80, height = 25)
        self.prog2.place(x = X//2 + 30, y = Y//2, width = 80, height = 25)

        self.settings_button = tk.Button(self, text = "Settings" , command = self.settings, font = main.button_font)
        self.settings_button.place(x = X//2 - 60, y = Y//2 + 80, width = 120, height = 40)

        self.logout_button = tk.Button(self, text = "Log out" , command = self.logout, font = main.button_font)
        self.logout_button.place(x = X//2 - 60, y = Y//2 + 150, width = 120, height = 40)

        self.pass_mode_button = tk.Button(self, text = "Pass Mode" , command = lambda : main.show_page(PassModePage.id), font = main.small_button_font)
        self.training_mode_button = tk.Button(self, text = "Training Mode" , command = lambda : main.show_page(TrainingModePage.id), font = main.small_button_font)
        self.rank_button = tk.Button(self, text = "Rank" , command = lambda : main.show_page(RankPage.id), font = main.small_button_font)
        self.my_button = tk.Button(self, text = "My" , command = lambda : main.show_page(MyPage.id), state=tk.DISABLED, font = main.small_button_font)
        self.pass_mode_button.place(x = X//2-360, y = Y//2+250, width = 120, height = 25)
        self.training_mode_button.place(x = X//2-160, y = Y//2+250, width = 120, height = 25)
        self.rank_button.place(x = X//2+40, y = Y//2+250, width = 120, height = 25)
        self.my_button.place(x = X//2+240, y = Y//2+250, width = 120, height = 25)

    def logout(self):
        user.logout()
        self.main.show_page(LoginPage.id)

    def get_info(self, event):
        username = user.get_user()
        self.name2["text"] = username
        score = user.get_score()
        self.score2["text"] = score
        prog = user.get_progress()
        self.prog2["text"] = f"Level {prog}"

    def settings(self):
        print(NotImplemented)


class LevelSelectionPage(tk.Frame):
    # DONE
    id = 8

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bind("<<OnRaise>>", self.get_progress)

        self.bg = tk.Label(self, image = imgs["pass_mode"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.back_button = tk.Button(self, text = "back" , command = lambda : main.show_page(PassModePage.id),  font = main.button_font)
        self.back_button.place(x = X//2 - 60, y = Y//2 + 150, width = 120, height = 40)

        self.levels = {}
        for i in range(5):
            self.levels[i] = tk.Button(self, text = f"Level {i}", command = (lambda x: lambda : self.level(x))(i), font = main.small_button_font, state=tk.DISABLED)
            self.levels[i].place(x = X//2 - 40, y = Y//2 - 140 + i*60, width = 80, height = 25)

    def get_progress(self, event):
        progress = user.get_progress()
        for i in range(min(progress+1, 5)):
            self.levels[i]["state"] = tk.NORMAL

    def level(self, level_id):
        self.main.show_page(BlankPage.id)
        mode = 0 # pass mode
        grade, score = GameController.game(mode, level_id)
        print (f"level: {level_id}")
        print(score, grade)
        user.add_score(score)
        if grade not in FAIL:
            # passed, update user progress
            progress = max(user.get_progress(), level_id+1)
            user.set_progress(progress)

        self.main.set_score_and_grade(score, grade)
        self.main.show_page(ResultPage.id)

class ResultPage(tk.Frame):
    # DONE
    id = 9

    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.main = main

        self.bg = tk.Label(self, image = imgs["result"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.bind("<<OnRaise>>", self.on_raise)

        self.grade = tk.StringVar()
        self.score = tk.StringVar()
        self.msg = tk.StringVar()

        self.grade_label = tk.Label(self, textvariable = self.grade, font = main.title_font)
        self.score_label = tk.Label(self, textvariable = self.score, font = main.title_font)
        self.msg_label = tk.Label(self, textvariable = self.msg, font = main.label_font)

        self.grade_label.place(x = X//2 - 50, y = Y//2 - 200, width = 100, height = 100)
        self.score_label.place(x = X//2 - 50, y = Y//2 - 70, width = 100, height = 100)
        self.msg_label.place(x = X//2 - 400, y = Y//2 + 60 , width = 800, height = 90)


        self.pass_msg = "Congratulations!\nYou did a great job to unlock the next level!"
        self.fail_msg = "Try again, you can do better"

        self.cont_button = tk.Button(self, text = "OK", command = lambda : main.show_page(LevelSelectionPage.id), font = main.button_font)
        self.cont_button.place(x = X//2 - 40, y = Y//2 + 160, width = 80, height = 40)

    def on_raise(self, event):
        score, grade = self.main.get_score_and_grade()
        self.grade.set(grade)
        self.score.set(score)
        if grade in FAIL:
            self.msg.set(self.fail_msg)
        else:
            self.msg.set(self.pass_msg)
        

class BlankPage(tk.Frame):
    # DONE
    id = 0
    def __init__(self, parent, main):
        X, Y = WINDOW_SIZE
        tk.Frame.__init__(self, parent, width = X, height = Y)
        self.bg = tk.Label(self, image = imgs["blank"])
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

    
####==== Main ====####

if __name__ == '__main__':
    app = JustMove()
    app.mainloop()

