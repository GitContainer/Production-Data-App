import snap7.client as c
from snap7.util import *
from snap7.snap7types import *
from time import sleep, strftime, gmtime, time
import mysql.connector
from datetime import date, datetime
from mysql.connector import errorcode

machines_status = {"SCHL4": False,
                    "SCHL5": False,
                    "SCHL7": False,
                    "JAGER": False,
                    "SCHL1": False,
                    "MG320":False,
                    "5S07": False,
                    "EVG": False,
                    "SCHL6": False} 

def ReadInput(plc,byte,bit,datatype = S7WLBit):
    result = plc.read_area(areas['PE'],0,byte,datatype)
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
    
def ReadOutput(plc,byte,bit,datatype = S7WLBit):
    result = plc.read_area(areas['PA'],0,byte,datatype)
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
    
def WriteOutput(plc,byte,bit,datatype,value):
    result = plc.read_area(areas['PA'],0,byte,datatype)
    if datatype==S7WLBit:
        set_bool(result,0,bit,value)
    elif datatype==S7WLByte or datatype==S7WLWord:
        set_int(result,0,value)
    elif datatype==S7WLReal:
        set_real(result,0,value)
    elif datatype==S7WLDWord:
        set_dword(result,0,value)
    plc.write_area(areas["PA"],0,byte,result)

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

def resetCounters():
    WriteMemory(plc,0,7,S7WLBit,False)

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

    machines_production = {"Schlatter 4": Sch4,
                            "Schlatter 5": Sch5,
                            "Schlatter 7": Sch7,
                            "Jager": Jager,
                            "Schlatter 1": Sch1,
                            "MG320": MG320,
                            "PG12": PG12}
    return machines_production

def gatherStopTime(plc):
    Sch4 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,60,0,S7WLDWord)))
    Sch5 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,64,0,S7WLDWord)))
    Sch7 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,68,0,S7WLDWord)))
    Jager = strftime('%H:%M:%S', gmtime(ReadMemory(plc,72,0,S7WLDWord)))
    Sch1 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,76,0,S7WLDWord)))
    MG320 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,80,0,S7WLDWord)))
    PG12 = strftime('%H:%M:%S', gmtime(ReadMemory(plc,84,0,S7WLDWord)))

    machines_stoptime = {"Schlatter 4": Sch4,
                            "Schlatter 5": Sch5,
                            "Schlatter 7": Sch7,
                            "Jager": Jager,
                            "Schlatter 1": Sch1,
                            "MG320": MG320,
                            "PG12": PG12}
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

    machines_velocities = {"Schlatter 4": Sch4,
                            "Schlatter 5": Sch5,
                            "Schlatter 7": Sch7,
                            "Jager": Jager,
                            "Schlatter 1": Sch1,
                            "MG320": MG320,
                            "PG12": PG12}
    return machines_velocities

def gatherStops(plc):
    Sch4 = ReadMemory(plc,108,0,S7WLWord)
    Sch5 = ReadMemory(plc,110,0,S7WLWord)
    Sch7 = ReadMemory(plc,112,0,S7WLWord)
    Jager = ReadMemory(plc,114,0,S7WLWord)
    Sch1 = ReadMemory(plc,116,0,S7WLWord)
    MG320 = ReadMemory(plc,118,0,S7WLWord)
    PG12 = ReadMemory(plc,120,0,S7WLWord)

    machines_stops = {"Schlatter 4": Sch4,
                            "Schlatter 5": Sch5,
                            "Schlatter 7": Sch7,
                            "Jager": Jager,
                            "Schlatter 1": Sch1,
                            "MG320": MG320,
                            "PG12": PG12}
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
    config = {
    'user': user,
    'password': password,
    'host': host,
    'database': database,
    'raise_on_warnings': True
    }    
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            status = "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            status = "Database does not exist"
        else:
            status = err
        return (0, status)
    else:
        status = "Connected"
        return (cnx, status)      

def addProduction(cursor, machines_production):
    D = {
      'SCHL4': machines_production["Schlatter 4"],
      'SCHL5': machines_production["Schlatter 5"],
      'SCHL7': machines_production["Schlatter 7"],
      'JAGER': machines_production["Jager"],
      'SCHL1': machines_production["Schlatter 1"],
      'MG320': machines_production["MG320"],
      '5S07': machines_production["PG12"],
      'EVG': 0,
      'SCHL6': 0
    }
    for key, value in D.items():
        if key != "EVG" and key != "SCHL6":
            query = ("UPDATE produccion_actual set golpes = %s where id_maquina = %s")
            values = (value, key)
            cursor.execute(query, values)

def addStopTime(cursor, machines_stoptime):
    D = {
      'SCHL4': machines_stoptime["Schlatter 4"],
      'SCHL5': machines_stoptime["Schlatter 5"],
      'SCHL7': machines_stoptime["Schlatter 7"],
      'JAGER': machines_stoptime["Jager"],
      'SCHL1': machines_stoptime["Schlatter 1"],
      'MG320': machines_stoptime["MG320"],
      '5S07': machines_stoptime["PG12"],
      'EVG': 0,
      'SCHL6': 0
    }
    for key, value in D.items():
        if key != "EVG" and key != "SCHL6":
            query = ("UPDATE produccion_actual set tiempo_paro = %s where id_maquina = %s")
            values = (value, key)
            cursor.execute(query, values)

def addVelocities(cursor, machines_velocities):
    D = {
      'SCHL4': machines_velocities["Schlatter 4"],
      'SCHL5': machines_velocities["Schlatter 5"],
      'SCHL7': machines_velocities["Schlatter 7"],
      'JAGER': machines_velocities["Jager"],
      'SCHL1': machines_velocities["Schlatter 1"],
      'MG320': machines_velocities["MG320"],
      '5S07': machines_velocities["PG12"],
      'EVG': 0,
      'SCHL6': 0
    }
    for key, value in D.items():
        if key != "EVG" and key != "SCHL6":
            query = ("UPDATE produccion_actual set velocidad = %s where id_maquina = %s")
            values = (value, key)
            cursor.execute(query, values) 

def addStartTimes(cursor, machines_status, machines_start):
    for key in machines_status.keys():
        if machines_status[key] == False and machines_start[key] == True:
            machines_status[key] = True
            hora = datetime.now().strftime('%H:%M.%S')
            query = ("UPDATE produccion_actual set inicio = %s where id_maquina = %s")
            values = (hora, key)
            cursor.execute(query, values)
    return machines_status

def addStops(cursor, machines_stops):
    D = {
      'SCHL4': machines_stops["Schlatter 4"],
      'SCHL5': machines_stops["Schlatter 5"],
      'SCHL7': machines_stops["Schlatter 7"],
      'JAGER': machines_stops["Jager"],
      'SCHL1': machines_stops["Schlatter 1"],
      'MG320': machines_stops["MG320"],
      '5S07': machines_stops["PG12"],
      'EVG': 0,
      'SCHL6': 0
    }
    for key, value in D.items():
        if key != "EVG" and key != "SCHL6":
            query = ("UPDATE produccion_actual set paros = %s where id_maquina = %s")
            values = (value, key)
            cursor.execute(query, values)

if __name__=="__main__":
    log = open("log.txt", 'a+')
    plc, statusPLC = connectPLC('192.168.8.100')
    if statusPLC == "Connected":
        cnx, statusSQL = connectSQL('root', 'Autom2018', '127.0.0.1', 'produccion')
        if statusSQL == "Connected":
            cursor = cnx.cursor()
            for i in range(50):
                machines_start = checkStart(plc)
                machines_status = addStartTimes(cursor, machines_status, machines_start)
                machines_production = gatherProductionData(plc)
                machines_stoptime = gatherStopTime(plc)
                machines_velocities = gatherVelocities(plc)
                machines_stops = gatherStops(plc)
                addProduction(cursor, machines_production)
                addStopTime(cursor, machines_stoptime)
                addVelocities(cursor, machines_velocities)
                addStops(cursor, machines_stops)
                cnx.commit()
            cursor.close()
            cnx.close()
            log.write("Data updated!")
            log.write("\n")
        else:
            log.write(statusSQL)
            log.write("\n")
    else:
        log.write(statusPLC)
        log.write("\n")
    log.close()
    
