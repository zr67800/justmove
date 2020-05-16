import openpyxl

def add(username,score):
        filePath="user&score.xlsx"
        flag = 0
        wb = openpyxl.load_workbook(filePath)
        ws = wb['Sheet']
        for i in ws:
            if i[0].value == username:
                i[1]+=score
                flag=1
                res = i[1]
                break
        if flag==0:
            ws.append([username, score])
            res = score
        wb.save(filePath)
        return res


def get(username):
        filePath="user&score.xlsx"
        flag = 0
        wb = openpyxl.load_workbook(filePath)
        ws = wb['Sheet']

        result = []
        for i in ws:
            result.append((i[0].value,int(i[1].value)))

        result.sort(key = lambda x: x[1], reverse = True)
        return result