import os
import sqlite3
import time

def dohoteltask(taskname, parameter):
    dbExists = os.path.isfile('cronhoteldb.db')

    dbcon = sqlite3.connect('cronhoteldb.db')
    with dbcon:
        cursor = dbcon.cursor()
        if dbExists:
            if(taskname == "clean"):
                roomsToClean = cursor.execute("Select RoomNumber from Residents Where FirstName ISNULL").fetchall()
                if roomsToClean is not None:
                    print("Rooms ")
                    for room in roomsToClean:
                        if(room == roomsToClean[len(roomsToClean)-1]):
                            timeToReturn = round(time.time(),2)
                            print(room + " were cleaned at " + str(timeToReturn) + "\n")
                            cursor.execute("update TaskTimes set NumTimes = NumTimes-1 Where TaskId = (select TaskId from Tasks where TaskName='clean')")
                            return timeToReturn
                        else:
                            print(room + ", ")
            else:
                person = cursor.execute("Select FirstName,LastName from Residents Where RoomNumber = ?",(parameter,)).fetchone()
                if person is not None:
                    if(taskname == "breakfast"):
                        timeToReturn = round(time.time(),2)
                        print(person[0] + " " + person[1] + " in room " + str(parameter) + " has been served breakfast at " + str(timeToReturn))
                        cursor.execute("update TaskTimes set NumTimes = NumTimes-1 Where TaskId = (select TaskId from Tasks where TaskName='breakfast' and Parameter=?)",(parameter,))
                        return timeToReturn
                    else:
                        timeToReturn = round(time.time(),2)
                        print(person[0] + " " + person[1] + " in room " + str(parameter) + " received a wakeup call at " + str(timeToReturn))
                        cursor.execute(
                            "update TaskTimes set NumTimes = NumTimes-1 Where TaskId = (select TaskId from Tasks where TaskName='wakeup' and Parameter=?)",(parameter,))
                        return timeToReturn