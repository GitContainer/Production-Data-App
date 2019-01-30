import snap7.client as c
from snap7.util import *
from snap7.snap7types import *
from time import sleep, strftime, gmtime, time
from datetime import date
import time as dt
import datetime
import psycopg2

machines_status = {"SCHL4": False,
                   "SCHL5": False,
                   "SCHL7": False,
                   "JAGER": False,
                   "SCHL1": False,
                   "MG320": False,
                   "5S07": False,
                   "EVG": False,
                   "SCHL6": False}

start_times = {}

def ReadMemory(plc, byte, bit, datatype):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        return get_bool(result, 0, bit)
    elif datatype == S7WLByte or datatype == S7WLWord:
        return get_int(result, 0)
    elif datatype == S7WLReal:
        return get_real(result, 0)
    elif datatype == S7WLDWord:
        return get_dword(result, 0)
    else:
        return None

def WriteMemory(plc, byte, bit, datatype, value):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        set_bool(result, 0, bit, value)
    elif datatype == S7WLByte or datatype == S7WLWord:
        set_int(result, 0, value)
    elif datatype == S7WLReal:
        set_real(result, 0, value)
    elif datatype == S7WLDWord:
        set_dword(result, 0, value)
    plc.write_area(areas["MK"], 0, byte, result)

def connectPLC(ipadress):
    plc = c.Client()
    try:
        plc.connect(ipadress, 0, 1)
    except:
        return (plc, "Connection to PLC failed")
    else:
        if plc.get_connected():
            return (plc, "Connected")
        else:
            return (plc, "Error: Unknown")

def gatherProductionData(plc):
    Sch4 = ReadMemory(plc, 28, 0, S7WLDWord)
    Sch5 = ReadMemory(plc, 4, 0, S7WLDWord)
    Sch7 = ReadMemory(plc, 8, 0, S7WLDWord)
    Jager = ReadMemory(plc, 12, 0, S7WLDWord)
    Sch1 = ReadMemory(plc, 16, 0, S7WLDWord)
    MG320 = ReadMemory(plc, 20, 0, S7WLDWord)
    PG12 = ReadMemory(plc, 24, 0, S7WLDWord)

    machines_production = {"SCHL4": Sch4,
                           "SCHL5": Sch5,
                           "SCHL7": Sch7,
                           "JAGER": Jager,
                           "SCHL1": Sch1,
                           "MG320": MG320,
                           "5S07": PG12}
    return machines_production

def gatherStartTime(plc, machine):
    if machine == "SCHL4":
        hour = ReadMemory(plc, 146, 0, S7WLWord)
        minute = ReadMemory(plc, 148, 0, S7WLWord)
        second = ReadMemory(plc, 150, 0, S7WLWord)
        return datetime.time(hour, minute, second)
    elif machine == "SCHL5":
        hour = ReadMemory(plc, 152, 0, S7WLWord)
        minute = ReadMemory(plc, 154, 0, S7WLWord)
        second = ReadMemory(plc, 156, 0, S7WLWord)
        return datetime.time(hour, minute, second)
    elif machine == "SCHL7":
        hour = ReadMemory(plc, 158, 0, S7WLWord)
        minute = ReadMemory(plc, 160, 0, S7WLWord)
        second = ReadMemory(plc, 162, 0, S7WLWord)
        return datetime.time(hour, minute, second)
    elif machine == "JAGER":
        hour = ReadMemory(plc, 134, 0, S7WLWord)
        minute = ReadMemory(plc, 136, 0, S7WLWord)
        second = ReadMemory(plc, 138, 0, S7WLWord)
        return datetime.time(hour, minute, second)
    elif machine == "SCHL1":
        hour = ReadMemory(plc, 140, 0, S7WLWord)
        minute = ReadMemory(plc, 142, 0, S7WLWord)
        second = ReadMemory(plc, 144, 0, S7WLWord)
        return datetime.time(hour, minute, second)
    elif machine == "MG320":
        hour = ReadMemory(plc, 122, 0, S7WLWord)
        minute = ReadMemory(plc, 124, 0, S7WLWord)
        second = ReadMemory(plc, 126, 0, S7WLWord)
        return datetime.time(hour, minute, second)
    elif machine == "5S07":
        hour = ReadMemory(plc, 128, 0, S7WLWord)
        minute = ReadMemory(plc, 130, 0, S7WLWord)
        second = ReadMemory(plc, 132, 0, S7WLWord)
        return datetime.time(hour, minute, second)

def gatherStopTime(plc):
    Sch4 = strftime('%H:%M:%S', gmtime(ReadMemory(plc, 60, 0, S7WLDWord)))
    Sch5 = strftime('%H:%M:%S', gmtime(ReadMemory(plc, 64, 0, S7WLDWord)))
    Sch7 = strftime('%H:%M:%S', gmtime(ReadMemory(plc, 68, 0, S7WLDWord)))
    Jager = strftime('%H:%M:%S', gmtime(ReadMemory(plc, 72, 0, S7WLDWord)))
    Sch1 = strftime('%H:%M:%S', gmtime(ReadMemory(plc, 76, 0, S7WLDWord)))
    MG320 = strftime('%H:%M:%S', gmtime(ReadMemory(plc, 80, 0, S7WLDWord)))
    PG12 = strftime('%H:%M:%S', gmtime(ReadMemory(plc, 84, 0, S7WLDWord)))

    machines_stoptime = {"SCHL4": Sch4,
                         "SCHL5": Sch5,
                         "SCHL7": Sch7,
                         "JAGER": Jager,
                         "SCHL1": Sch1,
                         "MG320": MG320,
                         "5S07": PG12}
    return machines_stoptime

def gatherVelocities(plc):
    Sch4 = float(ReadMemory(plc, 32, 0, S7WLDWord))
    if Sch4 != 0:
        Sch4 = int(60000 / Sch4)
    Sch5 = float(ReadMemory(plc, 36, 0, S7WLDWord))
    if Sch5 != 0:
        Sch5 = int(60000 / Sch5)
    Sch7 = float(ReadMemory(plc, 40, 0, S7WLDWord))
    if Sch7 != 0:
        Sch7 = int(60000 / Sch7)
    Jager = float(ReadMemory(plc, 44, 0, S7WLDWord))
    if Jager != 0:
        Jager = int(60000 / Jager)
    Sch1 = float(ReadMemory(plc, 48, 0, S7WLDWord))
    if Sch1 != 0:
        Sch1 = int(60000 / Sch1)
    MG320 = float(ReadMemory(plc, 52, 0, S7WLDWord))
    if MG320 != 0:
        MG320 = int(60000 / MG320)
    PG12 = float(ReadMemory(plc, 56, 0, S7WLDWord))
    if PG12 != 0:
        PG12 = int(60000 / PG12)

    machines_velocities = {"SCHL4": Sch4,
                           "SCHL5": Sch5,
                           "SCHL7": Sch7,
                           "JAGER": Jager,
                           "SCHL1": Sch1,
                           "MG320": MG320,
                           "5S07": PG12,
                           "EVG": 0,
                           "SCHL6": 0
                           }
    return machines_velocities

def gatherStops(plc):
    Sch4 = ReadMemory(plc, 108, 0, S7WLWord)
    Sch5 = ReadMemory(plc, 110, 0, S7WLWord)
    Sch7 = ReadMemory(plc, 112, 0, S7WLWord)
    Jager = ReadMemory(plc, 114, 0, S7WLWord)
    Sch1 = ReadMemory(plc, 116, 0, S7WLWord)
    MG320 = ReadMemory(plc, 118, 0, S7WLWord)
    PG12 = ReadMemory(plc, 120, 0, S7WLWord)

    machines_stops = {"SCHL4": Sch4,
                      "SCHL5": Sch5,
                      "SCHL7": Sch7,
                      "JAGER": Jager,
                      "SCHL1": Sch1,
                      "MG320": MG320,
                      "5S07": PG12}
    return machines_stops

def checkStart(plc):
    Sch4 = ReadMemory(plc, 106, 0, S7WLBit)
    Sch5 = ReadMemory(plc, 103, 1, S7WLBit)
    Sch7 = ReadMemory(plc, 106, 2, S7WLBit)
    Jager = ReadMemory(plc, 106, 3, S7WLBit)
    Sch1 = ReadMemory(plc, 106, 4, S7WLBit)
    MG320 = ReadMemory(plc, 106, 5, S7WLBit)
    PG12 = ReadMemory(plc, 106, 6, S7WLBit)

    machines_start = {"SCHL4": Sch4,
                      "SCHL5": Sch5,
                      "SCHL7": Sch7,
                      "JAGER": Jager,
                      "SCHL1": Sch1,
                      "MG320": MG320,
                      "5S07": PG12,
                      "EVG": False,
                      "SCHL6": False}
    return machines_start

def connectSQL(user, password, host, database):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host, database=database, user=user, password=password)
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        return (None, error)
    else:
        return (conn, cur)

def closeSQL(conn, cur):
    cur.close()
    conn.close()

def uploadData(cur, starts, stoptimes, stops, velocities, hits, hour):
    for key in machines_status.keys():
        if key != "SCHL6" and key != "EVG":
            if machines_status[key] == False and starts[key] == True:
                machines_status[key] = True
                start_times[key] = str(gatherStartTime(plc, key))
                query = ('UPDATE machines SET start_hour = %s where id = %s')
                values = (start_times[key], key)
                cur.execute(query, values)
            hourx = getHourPos()
            if hourx != -1:
                query = getQuery(hourx)
                values = (stoptimes[key], stops[key],
                          velocities[key], hits[key], hits[key], key)
                try:
                    cur.execute(query, values)
                except:
                    raise ValueError('Bad query')

def uploadVelocities(cur, velocities, hour):
    query = """INSERT INTO velocities 
    (timestamp, mg320, pg12, evg, jager, schl1, schl4, schl5, schl6, schl7)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (hour, velocities["MG320"], velocities["5S07"], velocities["EVG"], 
                velocities["JAGER"], velocities["SCHL1"], velocities["SCHL4"],
                velocities["SCHL5"], velocities["SCHL6"], velocities["SCHL7"])
    cur.execute(query, values)

def storeData(cur, shift, starts, stoptimes, stops, hits):
    date = dt.strftime("%A %d/%m/%Y")
    for key in machines_status.keys():
        if machines_status[key] is True:
            query = """INSERT INTO production 
                        (date, shift, machine, start_hour, stop_time, stops, hits)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            machine = getMachine(key)
            values = (date, shift, machine,
                      start_times[key], stoptimes[key], stops[key], hits[key])
            cur.execute(query, values)

def getMachine(id):
    D = {"SCHL4": "Schlatter 4",
         "SCHL5": "Schlatter 5",
         "SCHL7": "Schlatter 7",
         "JAGER": "Jager",
         "SCHL1": "Schlatter 1",
         "MG320": "MG320",
         "5S07": "PG12",
         "EVG": "EVG",
         "SCHL6": "Schlatter 6"}
    return D[id]

def getShift(plc):
    if ReadMemory(plc, 0, 0, S7WLBit):
        return 1
    elif ReadMemory(plc, 0, 1, S7WLBit):
        return 3
    else:
        return 0

def endOfShift(plc):
    return ReadMemory(plc, 1, 1, S7WLBit)

def AKS(plc):
    WriteMemory(plc, 0, 7, S7WLBit, True)

def resetAKS(plc):
    WriteMemory(plc, 0, 7, S7WLBit, False)

def emptyTable(cur):
    query = """UPDATE machines
                SET hits = 0,
                velocity = 0,
                stops = 0,
                stop_time = '00:00:00',
                start_hour = null,
                hour0 = 0,
                hour1 = 0,
                hour2 = 0,
                hour3 = 0,
                hour4 = 0,
                hour5 = 0,
                hour6 = 0,
                hour7 = 0,
                hour8 = 0,
                hour9 = 0"""
    cur.execute(query)
    query = "DELETE FROM velocities WHERE 1 = 1"
    cur.execute(query)

def getHourPos():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    day = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    night = [21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7]
    res = -1
    for i in range(11):
        if hour == day[i] or hour == night[i]:
            if minute >= 30:
                if hour != 17:
                    res = "hour" + str(i)
            else:
                if i == 0:
                    res = "hour9"
                else:
                    res = "hour" + str(i - 1)
            break
    return res

def getQuery(hourx):
    if hourx == "hour0":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour0 = %s
                    WHERE id = %s"""
    elif hourx == "hour1":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour1 = %s
                    WHERE id = %s"""
    elif hourx == "hour2":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour2 = %s
                    WHERE id = %s"""
    elif hourx == "hour3":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour3 = %s
                    WHERE id = %s"""
    elif hourx == "hour4":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour4 = %s
                    WHERE id = %s"""
    elif hourx == "hour5":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour5 = %s
                    WHERE id = %s"""
    elif hourx == "hour6":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour6 = %s
                    WHERE id = %s"""
    elif hourx == "hour7":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour7 = %s
                    WHERE id = %s"""
    elif hourx == "hour8":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour8 = %s
                    WHERE id = %s"""
    elif hourx == "hour9":
        query = """UPDATE machines 
                            SET stop_time = %s,
                                stops = %s,
                                velocity = %s,
                                hits = %s,
                                hour9 = %s
                    WHERE id = %s"""
    return query

if __name__ == "__main__":
    # log = open("log.txt", 'a+')
    plc, statusPLC = connectPLC('192.168.8.100')
    if statusPLC == "Connected":
        while True:
            if getShift(plc) != 0:
                conn, cur = connectSQL(
                    "postgres", "Autom2018", "localhost", "production_data")
                if conn:
                    emptyTable(cur)
                    conn.commit()
                    shift = getShift(plc)
                    i = 0
                    while True:
                        starts = checkStart(plc)
                        hits = gatherProductionData(plc)
                        stoptimes = gatherStopTime(plc)
                        velocities = gatherVelocities(plc)
                        stops = gatherStops(plc)
                        hour = datetime.datetime.now().strftime('%H:%M:%S')
                        if i % 5 == 0:
                            uploadVelocities(cur, velocities, hour)
                        uploadData(cur, starts, stoptimes,
                                   stops, velocities, hits, hour)
                        conn.commit()
                        if endOfShift(plc) == 1:
                            break
                        sleep(1)
                        i += 1
                    storeData(cur, shift, starts, stoptimes, stops, hits)
                    conn.commit()
                    AKS(plc)
                    while endOfShift(plc) == 1:
                        pass
                    resetAKS(plc)
                    closeSQL(conn, cur)
                    machines_status = {"SCHL4": False,
                                       "SCHL5": False,
                                       "SCHL7": False,
                                       "JAGER": False,
                                       "SCHL1": False,
                                       "MG320": False,
                                       "5S07": False,
                                       "EVG": False,
                                       "SCHL6": False}
                else:
                    # log.write(str(cur))
                    # log.write("\n")
                    pass
            else:
                sleep(30)
    else:
        # log.write(statusPLC)
        # log.write("\n")
        pass
    # log.close()