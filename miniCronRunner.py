import hotelWorker
import os
import sqlite3
import time

doneWork = False
if os.path.isfile('cronhoteldb.db'):
    dbcon = sqlite3.connect('cronhoteldb.db')
    seconds = 0
    with dbcon:
        cursor = dbcon.cursor()
        tasks = cursor.execute("SELECT Tasks.TaskName,Tasks.Parameter FROM Tasks JOIN TaskTimes ON Tasks.TaskId = TaskTimes.TaskId WHERE NumTimes > 0").fetchall()
        DoEveryList = cursor.execute("SELECT DISTINCT DoEvery FROM TaskTimes").fetchall()
        t0 = time.time()
        for task in tasks:
            lastTime = hotelWorker.dohoteltask(task[0], task[1])
        while (os.path.isfile('cronhoteldb.db')) and (not doneWork):
            t1 = time.time()
            total = t1 - t0
            time.sleep(1-total)
            t0 = time.time()
            seconds += 1
            for taskTime in DoEveryList:
                if seconds % taskTime[0] == 0:
                    tasksToOperate = cursor.execute("SELECT Tasks.TaskName,Tasks.Parameter FROM Tasks JOIN TaskTimes ON Tasks.TaskId = TaskTimes.TaskId WHERE ? % TaskTimes.DoEvery ==0  and NumTimes > 0", (seconds,)).fetchall()
                    for taskToOperate in tasksToOperate:
                        lastTime = hotelWorker.dohoteltask(taskToOperate[0], taskToOperate[1])
                    numRemainTasks = cursor.execute("SELECT sum(NumTimes) FROM TaskTimes").fetchone()
                    if numRemainTasks[0] == 0:
                        doneWork = True
                    break