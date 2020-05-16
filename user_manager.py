'''
user_manager.py

provide support for user signup, login, progress query
'''
import xlrd
import base64
import openpyxl
import hashlib

class UserManager:
    def __init__(self):
        self.active_user = None
        self.filePath = "user&pass.xlsx"

    def signup(self, username, password):
        assert self.active_user is None

        # save it to files
        
        wb = openpyxl.load_workbook(self.filePath)
        ws = wb['Sheet']
        for i in ws:
            print(i)
            if(username==i[0].value):
                print("This name has been used!")
                return False

        
        # md5
        m = hashlib.md5()
        m.update(password.encode("utf8"))
        ws.append([username,m.hexdigest(),0])
        wb.save(self.filePath)
        return True
        

    def login(self,username, password):
        assert self.active_user is None

        # verify user
        dataresult = []
        # needs to be encode
        sheetname = "Sheet"
        data_xlsl = xlrd.open_workbook(self.filePath)
        if not data_xlsl:
            raise IOError
        table = data_xlsl.sheet_by_name(sheetname)
        for i in range(0, table.nrows):
            dataresult.append(table.row_values(i))
        # print(dataresult)
        for i in dataresult:
            # print(str(base64.b64decode(i[1]),encoding="utf-8"))
            m = hashlib.md5()
            m.update(password.encode("utf8"))
            if(i[0]==username and i[1]==m.hexdigest()):
                self.active_user = username
                return True
        return False

    def get_user(self):
        return self.active_user
