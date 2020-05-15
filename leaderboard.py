import xlrd
import base64
import openpyxl

class leaderboard():
    def __init__(self):
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