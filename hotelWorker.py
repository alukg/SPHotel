import os
import sqlite3
import time

def dohoteltask(taskname, parameter):
    dbExists = os.path.isfile('cronhoteldb.db')
    dbCon = sqlite3.connect('cronhoteldb.db')
    with dbCon:
        cursor = dbCon.cursor()
        if dbExists:
            if taskname == "clean":
                roomsToClean = cursor.execute("Select Rooms.RoomNumber from Rooms EXCEPT SELECT Residents.RoomNumber FROM Residents").fetchall()
                if roomsToClean is not None:
                    print("Rooms"),
                    for room in roomsToClean:
                        if room == roomsToClean[len(roomsToClean)-1]:
                            timeToReturn = round(time.time(), 2)
                            print(str(room[0]) + " were cleaned at " + str(timeToReturn))
                            cursor.execute("update TaskTimes set NumTimes = NumTimes-1 Where TaskTimes.TaskId = (select TaskId from Tasks where TaskName='clean')")
                            return timeToReturn
                        else:
                            print(str(room[0]) + ","),
            else:
                person = cursor.execute("Select FirstName,LastName from Residents Where RoomNumber = ?",(parameter,)).fetchone()
                if person is not None:
                    if taskname == "breakfast":
                        timeToReturn = round(time.time(), 2)
                        print(person[0] + " " + person[1] + " in room " + str(parameter) + " has been served breakfast at " + str(timeToReturn))
                        cursor.execute("update TaskTimes set NumTimes = NumTimes-1 Where TaskTimes.TaskId = (select TaskId from Tasks where TaskName='breakfast' and Parameter=?)",(parameter,))
                        return timeToReturn
                    else:
                        timeToReturn = round(time.time(),2)
                        print(person[0] + " " + person[1] + " in room " + str(parameter) + " received a wakeup call at " + str(timeToReturn))
                        cursor.execute("update TaskTimes set NumTimes = NumTimes-1 Where TaskTimes.TaskId = (select TaskId from Tasks where TaskName='wakeup' and Parameter=?)",(parameter,))
                        return timeToReturn