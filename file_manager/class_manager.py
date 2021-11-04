import sqlite3, json
from PyQt5.QtCore import QDate, QTime
from file_manager.db_manager import DBManager
from util.datetimeutil import DateTimeUtil
# create the class manager class for this
db_file = "db/main.db"
class_time_file = "db/class_times.json"

class ClassManager:

    param = {
        "className" : ["className", "class_name", "classname", "ClassName", "clzName", "clz_name", "clzname"],
        "grade" : ["grade", "Grade", "gr"],
        "id" : ["index", "id", "i", "ID", "Id"],
        "subject" : ["subject", "Subject" , "sub"],
        "type" : ["type", "Type", "t"],
        "startDate" : ["date", "startDate", "start_date", "StartDate"]
    }

    @staticmethod
    def getKey(text: str):
        for key in ClassManager.param.keys():
            if (text in ClassManager.param.get(key)):
                return key

        return None

    def initiateTable(self):

        # create the table
        with DBManager(db_file, True) as cursor:
            cursor.execute(f"""CREATE TABLE class_table(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                        className TEXT NOT NULL,
                                                        grade INTEGER NOT NULL,
                                                        subject TEXT NOT NULL,
                                                        type TEXT NOT NULL,
                                                        cash FLOAT NOT NULL,
                                                        startDate TEXT NOT NULL)""")

        with open(class_time_file, "w") as file:
            json.dump({} , file, indent=4)

    def addClass(self, class_data : dict, db_file_ = db_file):

        name = class_data["className"]
        grade = class_data["grade"]
        sub = class_data["subject"]
        cash = class_data["cash"]

        type = "d" if class_data["type"].startswith("d") else "m"
        date = QDate.currentDate().toString("yyyy MM dd")

        with DBManager(db_file_, True) as cursor:
            cursor.execute(f"""INSERT INTO class_table(className , grade , subject , type , cash ,startDate)
                                VALUES('{name}' , {grade}, '{sub}', '{type}', {cash} ,'{date}')""")

    def getFromID(self, id : int):

        with DBManager(db_file) as cursor:
            cursor.execute(f"""SELECT * FROM class_table WHERE id = {id} """)
            data = cursor.fetchall()[0]

            return data

    def getClassNames(self, db_file_ = db_file):

        with DBManager(db_file_) as cursor:
            cursor.execute("SELECT className FROM class_table")
            data  = [item[0] for item in cursor.fetchall()]

            return data
        return []

    def getGrades(self, db_file_ = db_file):

        with DBManager(db_file_) as cursor:
            cursor.execute("SELECT grade FROM class_table")
            data = [int(item[0]) for item in cursor.fetchall()]

            return data
        return []

    def get(self, id : int , key  : str):

        key_ = ClassManager.getKey(key)

        if key_:
            with DBManager(db_file) as cursor:
                cursor.execute(f"""SELECT {key_} FROM class_table WHERE id = {id}""")
                try:
                    data = cursor.fetchall()[0][0]
                except:
                    data = []

                return data
        else:
            raise KeyError

    def getFromKey(self, key  : str):

        key_ = ClassManager.getKey(key)

        if key_:
            with DBManager(db_file) as cursor:
                cursor.execute(f"""SELECT {key} FROM class_table""")
                data = [i[0] for i in cursor.fetchall()]

                return data
        else:
            raise KeyError

    def getID(self, className : str , grade : int, db_file_ = db_file):

        with DBManager(db_file_) as cursor:
            cursor.execute(f"""SELECT id FROM class_table WHERE className = '{className}' AND grade = {grade} """)
            try:
                id = cursor.fetchall()[0][0]
            except:
                id = None

            return id

    def delete(self, id : int):

        try:
            with DBManager(db_file, True) as cursor:
                cursor.execute(f"""DELETE FROM class_table WHERE id = {id} """)
        except:
            raise IndexError

    def getClassWithGrades(self, db_file_ = db_file):

        with DBManager(db_file_) as cursor:
            cursor.execute(f"""SELECT className , grade FROM class_table """)
            data = [(item[0], int(item[1])) for item in cursor.fetchall()]

            return data

    def addTimeForClass(self, clz_id : int , week_day : int, start_time : QTime , end_time : QTime, class_times_file_ = class_time_file):

        if week_day > 7:
            raise IndexError
        # add to the class time file this times
        # based on the class id
        class_times = {}
        with open(class_times_file_) as file:
            class_times = json.load(file)

        # add the time to the class
        if class_times.get(str(clz_id), None):
            class_times.get(str(clz_id)).append((week_day , start_time.toString("hh:mm"), end_time.toString("hh:mm")))
        else:
            class_times[clz_id] = [(week_day , start_time.toString("hh:mm"), end_time.toString("hh:mm")), ]

        # save the file
        with open(class_times_file_, "w") as file:
            json.dump(class_times, file, indent=4)

    def isCrashTime(self, weeK_day : int, start_time : QTime , end_time : QTime, class_time_file_ = class_time_file) -> bool:

        # get the class times data
        class_times = {}
        with open(class_time_file_) as file:
            class_times = json.load(file)

        # use the loop
        isCrash = False
        for clz in class_times.keys():
            for times in class_times[clz]:
                # create the new time objects
                a, b = times[1].split(":")
                p, q = times[2].split(":")

                st_time = QTime(int(a), int(b))
                ed_time = QTime(int(p), int(q))

                if (DateTimeUtil.isCrash(st_time , ed_time , start_time , end_time)) and weeK_day == times[0]:
                    isCrash = True

        return isCrash

    def getClassTimes(self , clz_id : int, class_time_file_= class_time_file) -> list:

        class_times = {}
        with open(class_time_file_) as file:
            class_times = json.load(file)

        times = class_times.get(str(clz_id) , [])

        filter_times = []
        for t in times:
            # create the new time objects
            a, b = t[1].split(":")
            p, q = t[2].split(":")

            start_time = QTime(int(a), int(b))
            end_time = QTime(int(p), int(q))

            filter_times.append({
                "week_day" : t[0],
                "start_time" : start_time,
               "end_time" : end_time
            })

        return filter_times

    def getAllTimes(self):


        class_times = {}
        with open(class_time_file) as file:
            class_times = json.load(file)

        filter_times = []
        for times in class_times.keys():

            for t in class_times.get(times):
                # create the new time objects
                a, b = t[1].split(":")
                p, q = t[2].split(":")

                start_time = QTime(int(a), int(b))
                end_time = QTime(int(p), int(q))

                filter_times.append({
                    "week_day": t[0],
                    "start_time": start_time,
                    "end_time": end_time
                })

        return filter_times

    def isStartTime(self, week_day : int , start_time : QTime):

        if week_day > 7:
            raise IndexError

        class_times = {}
        with open(class_time_file) as file:
            class_times = json.load(file)

        for times in class_times:
            for time in class_times.get(times):
                st_time = time[1]
                if (int(st_time.split(":")[0]) == start_time.hour() and int(st_time.split(":")[1]) == start_time.minute() and week_day == time[0]):
                    return True

        return False

    def getTimesFromDay(self ,day_of_week : int, file = class_time_file):

        if day_of_week > 7:
            raise IndexError

        data = {}
        with open(file) as file:
            data = json.load(file)

        filter_data = []
        for i in data.keys():
            for item in data[i]:
                if item[0] == day_of_week:
                    filter_data.append((i, item[1], item[2]))
        del data

        # then decorate the data with names
        decorated_data = []
        for item in filter_data:
            name = self.get(item[0], "className")
            grade = self.get(item[0], "grade")

            decorated_data.append({
                "className" : name,
                "grade" : grade,
                "start_time" : item[1],
                "end_time" : item[2]
            })

        return decorated_data

    def getClassIDFromWeekDay(self, weeK_day : int = 1):

        if weeK_day > 7:
            raise IndexError

        with open(class_time_file) as file:
            data = json.load(file)

        # filter the data from the json data
        cls_ids = []
        for row in data.keys():
            i = 0
            for item in data[row]:
                if item[0] == weeK_day:
                    i += 1

            if i >= 1:
                cls_ids.append(int(row))

        return cls_ids

