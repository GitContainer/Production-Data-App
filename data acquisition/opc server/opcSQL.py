import snap7.client as c
from snap7.util import *
from snap7.snap7types import *
from time import sleep, strftime, gmtime, time
from datetime import date, datetime
import psycopg2

machines_status = {"SCHL4": False,
                    "SCHL5": False,
                    "SCHL7": False,
                    "JAGER": False,
                    "SCHL1": False,
                    "MG320":False,
                    "5S07": False,
                    "EVG": False,
                    "SCHL6": False} 

def ReadMemory(plc,byte,bit,datatype):
    result = plc.read_area(areas['MK'],0,byte,datatype)
    if datatype==S7WLBit:
        return get_bool(result,0,bit)
    elif datatype==S7WLByte or datatype==S7WLWord:
        return get_int(result,0)
    elif datatype==S7WLReal:
        return get_real(result,0)
    elif datatype==S7WLDWord:
        return get_dword(result,0)
    else:
        return None

def WriteMemory(plc,byte,bit,datatype,value):
    result = plc.read_area(areas['MK'],0,byte,datatype)
    if datatype==S7WLBit:
        set_bool(result,0,bit,value)
    elif datatype==S7WLByte or datatype==S7WLWord:
        set_int(result,0,value)
    elif datatype==S7WLReal:
        set_real(result,0,value)
    elif datatype==S7WLDWord:
        set_dword(result,0,value)
    plc.write_area(areas["MK"],0,byte,result)

def connectPLC(ipadress):
    plc = c.Client()
    try:
        plc.connect(ipadress,0,1)
    except:
        return (plc, "Connection to PLC failed")
    else:
        if plc.get_connected():
            return (plc, "Connected")
        else:
            return (plc, "Error: Unknown")
        
def gatherProductionData(plc):
    Sch4 = ReadMemory(plc,28,0,S7WLDWord)
    Sch5 = ReadMemory(plc,4,0,S7WLDWord)
    Sch7 = ReadMemory(plc,8,0,S7WLDWord)
    Jager = ReadMemory(plc,12,0,S7WLDWord)
    Sch1 = ReadMemory(plc,16,0,S7WLDWord)
    MG320 = ReadMemory(plc,20,0,S7WLDWord)
    PG12 = ReadMemory(plc,24,0,S7WLDWord)

    machines_production = {"SCHL4": Sch4,
                            "SCHL5": Sch5,
                            "SCHL7": Sch7,
                            "JAGER": Jager,
                            "SCHL1": Sch1,
                            "MG320": MG320,
                            "5S07": PG12}
    return machines_production

def gatherStopTime(plc):
    Sch4 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,60,0,S7WLDWord)))
    Sch5 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,64,0,S7WLDWord)))
    Sch7 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,68,0,S7WLDWord)))
    Jager = strftime('%H:%M:%S', gmtime(ReadMemory(plc,72,0,S7WLDWord)))
    Sch1 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,76,0,S7WLDWord)))
    MG320 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,80,0,S7WLDWord)))
    PG12 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,84,0,S7WLDWord)))

    machines_stoptime = {"SCHL4": Sch4,
                            "SCHL5": Sch5,
                            "SCHL7": Sch7,
                            "JAGER": Jager,
                            "SCHL1": Sch1,
                            "MG320": MG320,
                            "5S07": PG12}
    return machines_stoptime

def gatherVelocities(plc):
    Sch4 = float(ReadMemory(plc,32,0,S7WLDWord))
    if Sch4 != 0:
        Sch4 = int(60000 / Sch4)
    Sch5 = float(ReadMemory(plc,36,0,S7WLDWord))
    if Sch5 != 0:
        Sch5 = int(60000 / Sch5)
    Sch7 = float(ReadMemory(plc,40,0,S7WLDWord))
    if Sch7 != 0:
        Sch7 = int(60000 / Sch7)
    Jager = float(ReadMemory(plc,44,0,S7WLDWord))
    if Jager != 0:
        Jager = int(60000 / Jager)
    Sch1 = float(ReadMemory(plc,48,0,S7WLDWord))
    if Sch1 != 0:
        Sch1 = int(60000 / Sch1)
    MG320 = float(ReadMemory(plc,52,0,S7WLDWord))
    if MG320 != 0:
        MG320 = int(60000 / MG320)
    PG12 = float(ReadMemory(plc,56,0,S7WLDWord))
    if PG12 != 0:
        PG12 = int(60000 / PG12)

    machines_velocities = {"SCHL4": Sch4,
                            "SCHL5": Sch5,
                            "SCHL7": Sch7,
                            "JAGER": Jager,
                            "SCHL1": Sch1,
                            "MG320": MG320,
                            "5S07": PG12}
    return machines_velocities

def gatherStops(plc):
    Sch4 = ReadMemory(plc,108,0,S7WLWord)
    Sch5 = ReadMemory(plc,110,0,S7WLWord)
    Sch7 = ReadMemory(plc,112,0,S7WLWord)
    Jager = ReadMemory(plc,114,0,S7WLWord)
    Sch1 = ReadMemory(plc,116,0,S7WLWord)
    MG320 = ReadMemory(plc,118,0,S7WLWord)
    PG12 = ReadMemory(plc,120,0,S7WLWord)

    machines_stops = {"SCHL4": Sch4,
                        "SCHL5": Sch5,
                        "SCHL7": Sch7,
                        "JAGER": Jager,
                        "SCHL1": Sch1,
                        "MG320": MG320,
                        "5S07": PG12}
    return machines_stops

def checkStart(plc):
    Sch4 = ReadMemory(plc,106,0,S7WLBit)
    Sch5 = ReadMemory(plc,103,1,S7WLBit)
    Sch7 = ReadMemory(plc,106,2,S7WLBit)
    Jager = ReadMemory(plc,106,3,S7WLBit)
    Sch1 = ReadMemory(plc,106,4,S7WLBit)
    MG320 = ReadMemory(plc,106,5,S7WLBit)
    PG12 = ReadMemory(plc,106,6,S7WLBit)

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
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)   
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        return (None, error)
    else:
        return (conn, cur)

def closeSQL(conn, cur):
    cur.close()
    conn.close()

def uploadData(cur, starts, stoptimes, stops, velocities, hits):
    for key in machines_status.keys():
        if key != "SCHL6" and key!= "EVG":
            if machines_status[key] == False and starts[key] == True:
                machines_status[key] = True
                hour = datetime.now().strftime('%H:%M:%S')
                query = ('UPDATE machines SET start_hour = %s where id = %s')
                values = (hour, key)
                print(hour)
                print(str(hour))
                cur.execute(query, values)
                print(key)
                print(stops[key], velocities[key], hits[key])
            query = """UPDATE machines 
                        SET stop_time = %s,
                            stops = %s,
                            velocity = %s,
                            hits = %s
                        WHERE id = %s"""
            cur.execute(query, (stoptimes[key], stops[key], velocities[key], hits[key], key))

def endOfShift(plc):
    return ReadMemory(plc, 1, 1, S7WLBit)   

def AKS(plc):
    WriteMemory(plc, 0, 7, S7WLBit, True)

if __name__=="__main__":    
    log = open("log.txt", 'a+')
    plc, statusPLC = connectPLC('192.168.8.100')
    if statusPLC == "Connected":
        conn, cur = connectSQL("postgres", "Autom2018", "localhost", "production_data")
        if conn:
            while True:
                starts = checkStart(plc)
                hits = gatherProductionData(plc)
                stoptimes = gatherStopTime(plc)
                velocities = gatherVelocities(plc)
                stops = gatherStops(plc)
                uploadData(cur, starts, stoptimes, stops, velocities, hits)
                conn.commit()
                AKS(plc)
            closeSQL(conn, cur)
        else:
            log.write(str(cur))
            log.write("\n")
    else:
        log.write(statusPLC)
        log.write("\n")
    log.close()

    
