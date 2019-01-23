import datetime

now = datetime.datetime.now()
hour = now.hour
minute = now.minute

def getHourPos():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    res = 0
    for i in range(11):
        if hour == hours[i] or hour == hours[i] + 14:
            if minute >= 30:
                res = i
                break
            else:
                res = i - 1
                break
    if res == 0:
        return -2;
    else:
        return res

insertar en la columna Pos
