import snap7.client as c
from snap7.util import *
from snap7.snap7types import *
from time import sleep, strftime, gmtime, time
from datetime import date, time, timedelta
import time as dt
import datetime
import psycopg2
import locale
locale.setlocale(locale.LC_TIME, '')


def ReadMemory(plc, byte, bit, datatype):
    """ 
    Read internal memory variables from PLC.

    args:
        plc: plc object
        byte: byte in which data is stored
        bit: bit in which data is stored (in case of)
        datatype: variable data type (refer to snap7types)

    returns:
        Variable from plc.
    """
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
    """ 
    Write into internal memory variables of PLC.

    args:
        plc: plc object
        byte: byte in which data is stored
        bit: bit in which data is stored (in case of)
        datatype: variable data type (refer to snap7types)
        value: new value of variable
    """
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
    """ 
    Connects via OPC to plc.

    args:
        ipadress: ip adress of the plc's network card

    returns:
        plc: object with connection to plc
        status: Message with status of the connection to plc
    """
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


def reconnectPLC(plc, ipadress):
    """ 
    Re-establishes connection to PLC.

    args:
        plc: object with connection to plc

    returns:
        plc: new object with connection to plc
    """
    plc.disconnect()
    sleep(2)
    while True:
        print("Reconnecting to PLC...")
        try:
            plc.connect(ipadress, 0, 1)
        except:
            pass
        finally:
            sleep(2)
            if plc.get_connected():
                print("Reconnected!")
                break
    return plc


def getProductionData(plc):
    """ 
    Retrieves all the production (hits) of each machine.

    args:
        plc: plc object

    returns:
        Dictionary with each machine's hits
    """
    machines_production = {
        "SCHL4": ReadMemory(plc, 28, 0, S7WLDWord),
        "SCHL5": ReadMemory(plc, 4, 0, S7WLDWord),
        "SCHL7": ReadMemory(plc, 8, 0, S7WLDWord),
        "JAGER": ReadMemory(plc, 12, 0, S7WLDWord),
        "SCHL1": ReadMemory(plc, 16, 0, S7WLDWord),
        "MG320": ReadMemory(plc, 20, 0, S7WLDWord),
        "5S07": ReadMemory(plc, 24, 0, S7WLDWord)
    }
    return machines_production


def getStartTime(plc, machine):
    """ 
    Retrieves hour, time and second a machine start time.

    args:
        plc: plc object
        machine: the machine we want to get it's start time
    returns:
        Time object
    """
    try:
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
    except:
        return False


def getStopTime(plc):
    """ 
    Retrieves the time that each machine has been in stop state.

    args:
        plc: plc object

    returns:
        Dictionary with each machine's stop time.
    """
    machines_stoptime = {
        "SCHL4": strftime('%H:%M:%S', gmtime(ReadMemory(plc, 60, 0, S7WLDWord))),
        "SCHL5": strftime('%H:%M:%S', gmtime(ReadMemory(plc, 64, 0, S7WLDWord))),
        "SCHL7": strftime('%H:%M:%S', gmtime(ReadMemory(plc, 68, 0, S7WLDWord))),
        "JAGER": strftime('%H:%M:%S', gmtime(ReadMemory(plc, 72, 0, S7WLDWord))),
        "SCHL1": strftime('%H:%M:%S', gmtime(ReadMemory(plc, 76, 0, S7WLDWord))),
        "MG320": strftime('%H:%M:%S', gmtime(ReadMemory(plc, 80, 0, S7WLDWord))),
        "5S07": strftime('%H:%M:%S', gmtime(ReadMemory(plc, 84, 0, S7WLDWord)))
    }
    return machines_stoptime


def getVelocities(plc, old_velocities, stop_data, hour):
    """ 
    Retrieves in miliseconds the time between each hit of every machine and then
    it is converted to hits per minute. Also this function tells wether a machine
    is in stop state.

    args:
        plc: plc object
        old_velocities: dictionary containing the velocities of the last cycle

    returns:
        new_velocities: dictionary with each machine's velocity.
        in_stop_state: list with the key string of the machines in stop state.
    """
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

    new_velocities = {
        "SCHL4": Sch4,
        "SCHL5": Sch5,
        "SCHL7": Sch7,
        "JAGER": Jager,
        "SCHL1": Sch1,
        "MG320": MG320,
        "5S07": PG12,
        "SCHL6": 0
    }

    in_stop_state = []
    restarting = []

    for key, value in new_velocities.items():
        if value == 0 and old_velocities[key] > 0:
            stop_data[key]["start"] = hour
            in_stop_state.append(key)

        elif stop_data[key]["start"] != None and value > 0:
            stop_data[key]["end"] = hour
            restarting.append(key)

    return (new_velocities, in_stop_state, restarting, stop_data)


def getStops(plc):
    """ 
    Retrieves the number of times each machine has been in stop state.

    args:
        plc: plc object

    returns:
        Dictionary with each machine's number of stop states.
    """
    machines_stops = {
        "SCHL4": ReadMemory(plc, 108, 0, S7WLWord),
        "SCHL5": ReadMemory(plc, 110, 0, S7WLWord),
        "SCHL7": ReadMemory(plc, 112, 0, S7WLWord),
        "JAGER": ReadMemory(plc, 114, 0, S7WLWord),
        "SCHL1": ReadMemory(plc, 116, 0, S7WLWord),
        "MG320": ReadMemory(plc, 118, 0, S7WLWord),
        "5S07": ReadMemory(plc, 120, 0, S7WLWord)
    }
    return machines_stops


def checkStart(plc):
    """ 
    Checks if a machine has already started working.

    args:
        plc: plc object

    returns:
        Dictionary with the boolean state of each machine.
    """
    machines_start = {
        "SCHL4": ReadMemory(plc, 106, 0, S7WLBit),
        "SCHL5": ReadMemory(plc, 106, 1, S7WLBit),
        "SCHL7": ReadMemory(plc, 106, 2, S7WLBit),
        "JAGER": ReadMemory(plc, 106, 3, S7WLBit),
        "SCHL1": ReadMemory(plc, 106, 4, S7WLBit),
        "MG320": ReadMemory(plc, 106, 5, S7WLBit),
        "5S07": ReadMemory(plc, 106, 6, S7WLBit),
        "SCHL6": False
    }
    return machines_start


def connectSQL(user, password, host, database):
    """ 
    Connects to the server's data base.

    args:
        user: name of the data base manager
        password: password of the data base manager
        host: address in which the database is located
        database: the name of the data base we want to connect

    returns:
        cur: object that handles queries
        conn: object with connection to db
    """
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
    """
    Closes the connection to the database.

    args:
        cur: object that handles queries
        conn: object with connection to db
    """
    cur.close()
    conn.close()


def uploadData(cur, starts, stoptimes, stops, velocities, hits, hour, machines_status, start_times, in_stop_state, restarting, stop_data):
    """
    Uploads all the general data of every machine to the db every cycle.

    args:
        cur: object that handles queries
        starts: dictionary with the boolean state of each machine
        stoptimes: dictionary with the time of each machine being in stop state
        stops: dictionary withe the number of times each machine has been in stop state
        velocities: dictionary with the actual velocities of each machine
        hits: dictionary with the actual production of each machine
        hour: the time in which the actual cycle is being running
        machine_status: auxiliar boolean dictionary of each machine's "has started working" 
        start_times: dictionary with each machine's start times.
        in_stop_state: list with the machines that currently are in stop state

    returns:
        machine_status: auxiliar dictionary updated with each machine's "has started working" boolean state
        start_times: dictionary with each machine's start times updated.
    """
    for key in machines_status.keys():
        if key != "SCHL6":
            if machines_status[key] == False and starts[key] == True:
                start_time = getStartTime(plc, key)
                if not start_time == False:
                    start_times[key] = str(start_time)
                    machines_status[key] = True
                    query = ('UPDATE machines SET start_hour = %s where id = %s')
                    values = (start_times[key], key)
                    cur.execute(query, values)
            hourx = getHourPos()
            if hourx != -1:
                query = getQuery(hourx)
                values = (stoptimes[key], stops[key],
                          velocities[key], hits[key], hits[key], key)
                cur.execute(query, values)
            if key in in_stop_state:
                query = ('UPDATE machines SET last_stop = %s where id = %s')
                values = (hour, key)
                cur.execute(query, values)
            elif key in restarting:
                query = """INSERT INTO stops_record (date, start_stop, duration, minutes_duration, machine)
	                        VALUES (%s, %s, %s, %s, %s);"""
                today = dt.strftime("%A %d/%m/%Y")
                start_stop = stop_data[key]["start"]
                end_stop = stop_data[key]["end"]
                try:
                    duration = (end_stop - start_stop)
                except:
                    print("Duration error None Type")
                else:
                    total_seconds = duration.total_seconds()
                    hours = int(total_seconds / 3600)
                    minutes = int((-hours * 3600 + total_seconds) / 60)
                    seconds = int(total_seconds - hours * 3600 - minutes * 60)
                    duration = datetime.time(hours, minutes, seconds)
                    minutes_duration = total_seconds / 60
                    values = (today, start_stop.strftime("%H:%M:%S"), duration, minutes_duration, key)
                    stop_data[key]["start"] = None
                    stop_data[key]["end"] = None
                    restarting.remove(key)
                    cur.execute(query, values)
                
    return (machines_status, start_times, stop_data)


def uploadVelocities(cur, velocities, hour):
    """
    Uploads the actual velocity of each machine with a time stamp to the db

    args:
        cur: object that handles queries
        velocities: dictionary with each machine's velocities
        hour: actual cycle local time
    """
    query = """INSERT INTO velocities 
    (timestamp, mg320, pg12, jager, schl1, schl4, schl5, schl6, schl7)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (hour, velocities["MG320"], velocities["5S07"],
              velocities["JAGER"], velocities["SCHL1"], velocities["SCHL4"],
              velocities["SCHL5"], velocities["SCHL6"], velocities["SCHL7"])
    cur.execute(query, values)


def storeData(cur, shift, stoptimes, stops, hits, machines_status, start_times):
    """
    Uploads all the important production data to db at the end of every shift with the date

    args:
        cur: object that handles queries
        shift: number of shift (1: morning, 2: evening, 3: night)
        stoptimes: dictionary with the time of each machine being in stop state
        stops: dictionary withe the number of times each machine has been in stop state
        hits: dictionary with the actual production of each machine
        machine_status: auxiliar boolean dictionary of each machine's "has started working"
        start_times: dictionary with each machine's start times.
    """
    if shift == 3:
        date1 = (date.today() - timedelta(days=1)).strftime("%A %d/%m/%Y")
    else:
        date1 = dt.strftime("%A %d/%m/%Y")
    for key in machines_status.keys():
        if machines_status[key] is True:
            query = """INSERT INTO production 
                        (date, shift, machine, start_hour, stop_time, stops, hits)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            machine = getMachine(key)
            values = (date1, shift, machine,
                      start_times[key], stoptimes[key], stops[key], hits[key])
            cur.execute(query, values)


def getMachine(id):
    """
    Gets the name of a machine.

    args:
        id: key string of a machine

    returns:
        String containing the machine's name.
    """
    D = {
        "SCHL4": "Schlatter 4",
        "SCHL5": "Schlatter 5",
        "SCHL7": "Schlatter 7",
        "JAGER": "Jager",
        "SCHL1": "Schlatter 1",
        "MG320": "MG320",
        "5S07": "PG12",
        "SCHL6": "Schlatter 6"
    }
    return D[id]


def getShift(plc):
    """
    Gets the shift number from plc

    args:
        plc: plc object with connection to real plc

    returns:
        Shift integer (1: morning, 2: evening, 3: night)
    """
    try:
        if ReadMemory(plc, 0, 0, S7WLBit):
            return (1, plc)
        elif ReadMemory(plc, 0, 1, S7WLBit):
            return (3, plc)
        else:
            return (0, plc)
    except:
        plc = reconnectPLC(plc, '192.168.8.100')
        return (-1, plc)


def endOfShift(plc):
    """Gets a boolean from plc indicating if the shift has ended"""
    try:
        return (ReadMemory(plc, 1, 1, S7WLBit), plc)
    except:
        plc = reconnectPLC(plc, '192.168.8.100')
        return (-1, plc)


def AKS(plc):
    """Python tells plc that the data has been stored succesfully so the plc can erase it"""
    try:
        WriteMemory(plc, 0, 7, S7WLBit, True)
        return (True, plc)
    except:
        plc = reconnectPLC(plc, '192.168.8.100')
        return (False, plc)


def resetAKS(plc):
    """Reset AKS variable of the plc"""
    try:
        WriteMemory(plc, 0, 7, S7WLBit, False)
        return (True, plc)
    except:
        plc = reconnectPLC(plc, '192.168.8.100')
        return (False, plc)


def emptyTable(cur):
    """Erase all the values in the db tables"""
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
                hour9 = 0, 
                last_stop = null"""
    cur.execute(query)
    query = "DELETE FROM velocities WHERE 1 = 1"
    cur.execute(query)


def getHourPos():
    """Gets the number of actual hour (First hour, second hour, etc...)"""
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
    """Auxiliar function that returns a string query based in the actual hour number (see getHourPos)"""
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
    while True:
        print("Not connected")
        # Connect to PLC
        plc, statusPLC = connectPLC('192.168.8.100')
        if statusPLC == "Connected":
            print("Connected to PLC")
            while True:
                print("Checking for shift")
                # Get shift number from plc
                shift, plc = getShift(plc)
                if shift > 0:
                    print("Time to work!, connecting to db")
                    # Connect to data base
                    conn, cur = connectSQL(
                        "postgres", "4RM453LDB", "localhost", "production_data")
                    if conn:
                        print("Connected to db")
                        # Erase dynamic table content
                        emptyTable(cur)
                        conn.commit()
                        print("Cleared table")
                        # Initialize dictionaries
                        machines_status = {
                            "SCHL4": False,
                            "SCHL5": False,
                            "SCHL7": False,
                            "JAGER": False,
                            "SCHL1": False,
                            "MG320": False,
                            "5S07": False,
                            "SCHL6": False
                        }
                        velocities = {
                            "SCHL4": 0,
                            "SCHL5": 0,
                            "SCHL7": 0,
                            "JAGER": 0,
                            "SCHL1": 0,
                            "MG320": 0,
                            "5S07": 0,
                            "SCHL6": 0
                        }
                        start_times = {}
                        stop_data = {
                            "MG320": {
                                "start": None,
                                "end": None
                            },
                            "5S07": {
                                "start": None,
                                "end": None
                            },
                            "JAGER": {
                                "start": None,
                                "end": None
                            },
                            "SCHL1": {
                                "start": None,
                                "end": None
                            },
                            "SCHL4": {
                                "start": None,
                                "end": None
                            },
                            "SCHL5": {
                                "start": None,
                                "end": None
                            },
                            "SCHL6": {
                                "start": None,
                                "end": None
                            },
                            "SCHL7": {
                                "start": None,
                                "end": None
                            }
                        }
                        i = 0
                        print("Getting data from PLC and updating db...")
                        while True:
                            hour = datetime.datetime.now()
                            # Get all data from PLC
                            try:
                                starts = checkStart(plc)
                                hits = getProductionData(plc)
                                stoptimes = getStopTime(plc)
                                stops = getStops(plc)
                                if i % 5 == 0:
                                    velocities, in_stop_state, restarting, stop_data = getVelocities(plc, velocities, stop_data, hour)
                            except:
                                print("Error while getting data from PLC")
                                plc = reconnectPLC(plc, '192.168.8.100')
                            # If successful, update data base
                            else:
                                hour = hour.strftime('%H:%M:%S')
                                if i % 5 == 0:
                                    uploadVelocities(cur, velocities, hour)
                                machines_status, start_times, stop_data = uploadData(cur, starts, stoptimes, stops, velocities, hits, hour, machines_status, start_times, in_stop_state, restarting, stop_data)
                                conn.commit()
                            # If shift has ended, break loop
                            end_of_shift, plc = endOfShift(plc)
                            while end_of_shift == -1:
                                end_of_shift, plc = endOfShift(plc)
                            if end_of_shift:
                                print("End of shift")
                                break
                            sleep(1)
                            i += 1
                        # Store important data of shift to data base
                        print("Storing data")
                        storeData(cur, shift, stoptimes, stops,
                                  hits, machines_status, start_times)
                        conn.commit()
                        # Wait until python succesfully sends AKS
                        print("Sending AKS")
                        success_status, plc = AKS(plc)
                        while success_status == False:
                            success_status, plc = AKS(plc)
                        # Wait until python succesfully receives answer from PLC
                        print("Waiting for response")
                        end_of_shift, plc = endOfShift(plc)
                        while end_of_shift == -1 or end_of_shift == 1:
                            end_of_shift, plc = endOfShift(plc)
                        # Wait until python succesfully resets AKS variable
                        print("Resetting AKS")
                        success_status, plc = resetAKS(plc)
                        while success_status == False:
                            success_status, plc = resetAKS(plc)
                        # Close connection to data base
                        closeSQL(conn, cur)
                        print("Closed connection to db")
                    else:
                        print("Couldn't connect to db")
                elif shift == -1:
                    pass
                else:
                    print("Sleeping")
                    # Sleep for 30 seconds meanwhile there is no activity
                    sleep(30)
        else:
            sleep(2)
