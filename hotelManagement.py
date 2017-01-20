
import os
import sqlite3

dbExists = os.path.isfile('cronhoteldb.db')

dbcon = sqlite3.connect('cronhoteldb.db')
with dbcon:
    cursor = dbcon.cursor()
    if not dbExists:
        i = 0
        cursor.execute("CREATE TABLE TaskTimes(TaskId INTEGER PRIMARY KEY NOT NULL,DoEvery INTEGER NOT NULL, NumTimes INTEGER NOT NULL)")
        cursor.execute("CREATE TABLE Tasks(TaskId INTEGER REFERENCES TaskTimes(TaskId),TaskName TEXT NOT NULL, Parameter INTEGER)")
        cursor.execute("CREATE TABLE Rooms(RoomNumber INTEGER PRIMARY KEY NOT NULL)")
        cursor.execute("CREATE TABLE Residents(RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber),FirstName TEXT NOT NULL, LastName TEXT NOT NULL)")

        with open("config.txt") as config:
            content = config.readlines()
            content = [x.strip() for x in content]
            for line in content:
                splitline = line.split(',')
                if splitline[0] == "room":
                    cursor.execute("INSERT INTO Rooms VALUES (?)",(splitline[1],))
                    if(len(splitline)>2):
                        cursor.execute("INSERT INTO Residents VALUES (?,?,?)", (splitline[1],splitline[2],splitline[3],))
                else:
                    if(len(splitline) == 3):
                        cursor.execute("INSERT INTO TaskTimes VALUES (?,?,?)", (i,splitline[1],splitline[2],))
                        cursor.execute("INSERT INTO Tasks VALUES (?,?,?)", (i,splitline[0], 0,))
                        i= i+1
                    else:
                        cursor.execute("INSERT INTO TaskTimes VALUES (?,?,?)", (i, splitline[1], splitline[3],))
                        cursor.execute("INSERT INTO Tasks VALUES (?,?,?)", (i, splitline[0], splitline[2],))
                        i=i+1





