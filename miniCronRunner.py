import hotelWorker
import os
import sqlite3
import time

doneWork = False
dbcon = sqlite3.connect('cronhoteldb.db')
seconds = 0
with dbcon:
    cursor = dbcon.cursor()
    tasks = cursor.execute("SELECT Tasks.TaskName,Tasks.Parameter FROM Tasks JOIN TaskTimes ON Tasks.TaskId = TaskTimes.TaskId WHERE NumTimes > 0").fetchall()
    for task in tasks:
        lasttime = hotelWorker.dohoteltask(task[0],task[1])
    list = cursor.execute("SELECT DISTINCT DoEvery FROM TaskTimes").fetchall()
    while (os.path.isfile('cronhoteldb.db')) and (not doneWork):
        time.sleep(1)
        seconds = seconds+1
        for taskTime in list:
            if(seconds % taskTime[0] == 0):
                taskstoOperate = cursor.execute("SELECT Tasks.TaskName,Tasks.Parameter FROM Tasks JOIN TaskTimes ON Tasks.TaskId = TaskTimes.TaskId WHERE MOD(?,TaskTimes.DoEvery) ==0  and NumTimes > 0",(seconds,)).fetchall()
                for tasktoOperate in taskstoOperate:
                    lasttime = hotelWorker.dohoteltask(tasktoOperate[0],tasktoOperate[1])


        numTasks = cursor.execute("SELECT sum(NumTimes) FROM TaskTimes").fetchone()
        if(numTasks[0] == 0):
            doneWork = True