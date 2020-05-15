'''
JUST MOVE -- an fitness game app prototype with camera based human posture recognition.


This is the entry point of the game. To run the game, use Python 3.8+ with opencv. 
    python main_UI.py

This file includes the main part of the UI control and navigation.

'''


import tkinter as tk
import tkinter.font as tkFont
from tkinter import StringVar
import tkinter.messagebox as messagebox
import game_controller as GameController
import xlrd
import base64
import openpyxl
####==== dummy component ====####

# #from game_controller import GameController
# import time
# class GameController:

#     def game(mode, id):
#         print (f"mode = {mode}, id = {id}")
#         for i in range(5,0, -1):
#             print(i)
#             time.sleep(1)
#         return 100, "A"


#from userdata import UserManager
class UserManager:

    def signup(username, password):
        # save it to files
        filePath = "user&pass.xlsx"
        flag=0
        wb = openpyxl.load_workbook(filePath)
        ws = wb['Sheet']
        for i in ws:
            print(i)
            if(username==i[0]):
                print("This name has been used!")
                flag=1

        if(flag==0):
            ws.append([username,base64.b64encode(password)])
            wb.save(filePath)
            return True
        else:
            return False
    def login(username, password):
        # verify user
        dataresult = []
        # needs to be encode
        filePath = "user&pass.xlsx"
        sheetname = "Sheet"
        data_xlsl = xlrd.open_workbook(filePath)
        if not data_xlsl:
            return False
        table = data_xlsl.sheet_by_name(sheetname)
        for i in range(0, table.nrows):
            dataresult.append(table.row_values(i))
        # print(dataresult)
        for i in dataresult:
            print(str(base64.b64decode(i[1]),encoding="utf-8"))
            if(i[0]==username and str(base64.b64decode(i[1]),encoding="utf-8")==password):
                return True
        return False
class leaderboard():
    def __init__(self):
        #
        self.list=[]
    def set(username,score):
        filePath="user&score.xlsx"
        flag = 0
        wb = openpyxl.load_workbook(filePath)
        ws = wb['Sheet1']
        for i in ws:
            i[1]+=score
            flag=1
        if flag==0:
            ws.append([username, score])
            wb.save(filePath)
        return True


    def get(username):
        dataresult = []
        # needs to be encode
        filePath = "user&score.xlsx"
        sheetname = "Sheet1"
        data_xlsl = xlrd.open_workbook(filePath)
        if not data_xlsl:
            return False
        table = data_xlsl.sheet_by_name(sheetname)
        for i in range(0, table.nrows):
            dataresult.append(table.row_values(i))
        dic = {dataresult[i]:dataresult[i+1] for i in range(0,len(dataresult),2)}
        keys = dic.keys()
        keys.sort()
        return map(dic.get, keys)

        #keys = dic.keys()
        #keys.sort()
        #return map(dic.get, keys)
    # def RankInOneLevel(self,username,score):


####==== Meta parameters ====####

# This is for desktop
WINDOW_SIZE = (1280, 720)

# failing grades
FAIL = {"F"}


####==== Classes ====####

class JustMove(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.window = tk.Tk()
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
            # init every pages
            page_id = F.id 
            frame = F(self.main_window, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[page_id] = frame

        self.current_result = None

        self.show_page(WelcomePage.id)
    # show pages based page id
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
        # window = tk.Tk()
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
        print(allowed)
        if allowed:
            print("Login secsessful!")
            self.main.show_page(PassModePage.id)
        else:
            # TODO: handel wrong password/non existing username
            messagebox.showinfo(title="error", message="Your username or password is incorrect!")
            self.main.show_page(LoginPage.id)

class SignUpPage(tk.Frame):
    id = 3
    # needs future decorate
    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
        self.main = main

        self.back_button = tk.Button(self, text = "back" , command = lambda : main.show_page(LoginPage.id), font = main.button_font)
        self.back_button.grid(row=0,column=0,sticky="NW")
        tk.Label(self, text='Username:', font=main.button_font).place(x=400, y=150)
        self.username = StringVar()
        entry_usr_name = tk.Entry(self, textvariable=self.username)
        entry_usr_name.place(x=600, y=150)
        tk.Label(self, text='Password:', font=main.button_font).place(x=400, y=200)
        self.password = StringVar()
        entry_password = tk.Entry(self,textvariable=self.password)
        entry_password.place(x=600,y=200)

        self.registerButton=tk.Button(self, text = "Sign Up", command = self.signup, font = main.button_font)
        self.registerButton.place(x=600,y=300)


        # TODO
    def signup(self):
        username_ = self.username.get()
        password_ = self.password.get()
        register = UserManager.signup(username=username_, password=password_)
        if register:
            self.main.show_page(LoginPage.id)
        else:
            messagebox.showinfo(title="error", message="Registration failed")
            self.main.show_page(SignUpPage.id)

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
        # one level get one resultpage so how to show different content
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
    #def add(self,username,score):

    # excel to record username-grades






class BlankPage(tk.Frame):
    id = 0
    def __init__(self, parent, main):
        tk.Frame.__init__(self, parent, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1])
    
####==== Main ====####

if __name__ == '__main__':
    app = JustMove()
    app.mainloop()

