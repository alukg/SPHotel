import os
import sqlite3

dbExists = os.path.isfile('cronhoteldb.db')

dbCon = sqlite3.connect('cronhoteldb.db')
with dbCon:
    cursor = dbCon.cursor()
    if not dbExists:
        i = 0
        cursor.execute("""CREATE TABLE TaskTimes(
                              TaskId INTEGER PRIMARY KEY NOT NULL,
                              DoEvery INTEGER NOT NULL,
                              NumTimes INTEGER NOT NULL)""")

        cursor.execute("""CREATE TABLE Tasks(
                              TaskId INTEGER REFERENCES TaskTimes(TaskId),
                              TaskName TEXT NOT NULL,
                              Parameter INTEGER)""")

        cursor.execute("""CREATE TABLE Rooms(
                              RoomNumber INTEGER PRIMARY KEY NOT NULL)""")

        cursor.execute("""CREATE TABLE Residents(
                              RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber),
                              FirstName TEXT NOT NULL,
                              LastName TEXT NOT NULL)""")

        with open("config.txt") as config:
            content = config.readlines()
            content = [x.strip() for x in content]
            for line in content:
                splitLine = line.split(',')
                if splitLine[0] == "room":
                    cursor.execute("INSERT INTO Rooms VALUES (?)", (splitLine[1],))
                    if len(splitLine) > 2:
                        cursor.execute("INSERT INTO Residents VALUES (?,?,?)", (splitLine[1], splitLine[2], splitLine[3],))
                else:
                    if len(splitLine) == 3:
                        cursor.execute("INSERT INTO TaskTimes VALUES (?,?,?)", (i, splitLine[1], splitLine[2],))
                        cursor.execute("INSERT INTO Tasks VALUES (?,?,?)", (i, splitLine[0], 0,))
                        i += 1
                    else:
                        cursor.execute("INSERT INTO TaskTimes VALUES (?,?,?)", (i, splitLine[1], splitLine[3],))
                        cursor.execute("INSERT INTO Tasks VALUES (?,?,?)", (i, splitLine[0], splitLine[2],))
                        i += 1