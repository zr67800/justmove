import xlrd
import base64
import openpyxl
import hashlib

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
            # md5
            m = hashlib.md5()
            m.update(password.encode("utf8"))
            ws.append([username,m.hexdigest()])
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
            # print(str(base64.b64decode(i[1]),encoding="utf-8"))
            m = hashlib.md5()
            m.update(password.encode("utf8"))
            if(i[0]==username and i[1]==m.hexdigest()):
                return True
        return False