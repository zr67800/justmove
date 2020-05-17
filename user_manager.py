'''
user_manager.py

provide support for user signup, login, progress query, and leaderboard
'''

import os
import json
import hashlib

class UserManager:
    def __init__(self):
        self.file_path = "./data/user.json"
        if not os.path.exists("./data/"):
            os.makedirs("./data/")
        try:
            with open(self.file_path, 'r') as file:
                pass
        except:
            with open(self.file_path, "w") as file:
                json.dump({"-":{"password": 0, "score": 0, "progress": 0}},file)

        self.active_user = None
        self.working_data = None #dict[username] of dict {password, score, progress}


    def _load(self):
        with open(self.file_path, 'r') as json_file:
            self.working_data = json.load(json_file)
    def _save(self):
        with open(self.file_path, 'w') as json_file:
            json.dump(self.working_data, json_file)
    def _encode(self, pwd):
        m = hashlib.md5()
        m.update(str(pwd).encode("utf8"))
        return m.hexdigest()
    
    
    def signup(self, username, password):
        self._load()
        if username in self.working_data:
            print("This name has been used!")
            return False
        self.working_data[username] = {}
        self.working_data[username]["password"] = self._encode(password)
        self.working_data[username]["score"] = 0
        self.working_data[username]["progress"] = 0
        self._save()
        return True
            

    def login(self,username, password):
        self._load()
        if username in self.working_data:
            if self.working_data[username]["password"] == self._encode(password):
                self.active_user = username
                return True

    def get_user(self):
        return self.active_user

    def logout(self):
        self.active_user = None

    def get_progress(self):
        self._load()
        username = self.active_user
        if username not in self.working_data:
            raise IOError
        return self.working_data[username]["progress"]


    def set_progress(self, progress):
        self._load()
        username = self.active_user
        if username not in self.working_data:
            raise IOError
        self.working_data[username]["progress"] = progress
        self._save()

    def add_score(self, score):
        self._load()
        username = self.active_user
        if username not in self.working_data:
            raise IOError
        self.working_data[username]["score"] += score
        self._save()

    def get_score(self):
        self._load()
        username = self.active_user
        if username not in self.working_data:
            raise IOError
        return self.working_data[username]["score"]

    def get_leaderboard(self):
        self._load()
        res = []
        for username in self.working_data:
            if username != "-":
                res.append([username, self.working_data[username]["score"]])
        res.sort(key = lambda x: x[1], reverse = True)
        return res


if __name__ == "__main__":
    u = UserManager()
    u.signup("qwerty", 123456)
    u.login("qwerty", 123456)
    print(u.get_progress())
    u.set_progress(5)
    print(u.get_progress())
    u.add_score(10)
    print(u.get_score())
    u.add_score(100)
    print(u.get_score())
    print(u.get_leaderboard())