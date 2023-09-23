import sqlite3, json, csv, os
from file_manager.db_manager import  DBManager
from PyQt5.QtCore import QDate, QTime

class_root_path = "db/classes"
db_file = "db/main.db"

class ClassInitializer:
    
    def isValidClzID(self, id : int):
        
        with DBManager(db_file) as cursor:
            cursor.execute("""SELECT id FROM class_table""")
            
            data = [i[0] for i in cursor.fetchall()]
            
            if id in data:
                return True
            return False
    
    def initializeClass(self, clz_id  : int , year : int , std_ids : list):
        
        # create the new json file for this class
        if not self.isValidClzID(clz_id):
            raise IndexError

        data = {
            "clz_id" : clz_id,
            "year" : year,
            "students" : std_ids
        }

        # create the new json file for this
        file_name = f"{year}@{clz_id}@class.json"
        with open(os.path.join(class_root_path , file_name) , "w") as file:
            json.dump(data ,file, indent=4)

        # create the class history json data file for tracked th class
        history_file_name = f"{year}@{clz_id}@classhistory.json"
        with open(os.path.join("db/classes_history", history_file_name), "w") as file:
            json.dump([], file, indent=4)

        # create the new file for registers as the csv file
        csv_file_name = f"{year}@{clz_id}@class_register.csv"
        writer = csv.DictWriter(open(os.path.join(class_root_path , csv_file_name) , "w"), fieldnames=["date", "student_id", "state"])
        writer.writeheader()

        del writer

    def addStudentsToClass(self, clz_id : int , year : int , std_list : list):

        if not self.isValidClzID(clz_id):
            raise IndexError

        file_name = f"{year}@{clz_id}@class.json"
        with open(os.join(class_root_path, file_name)) as file:
            class_data = json.load(file)

        class_data["students"] = [ *class_data["students"] , *std_list]

        with open(os.join(class_root_path, file_name) ,"w") as file:
            json.dump(class_data, file, indent=4)

    def getClassStudents(self, clz_id  : int , year : int) -> list:

        if not self.isValidClzID(clz_id):
            raise IndexError

        file_name = f"{year}@{clz_id}@class.json"
        with open(os.path.join(class_root_path, file_name)) as file:
            class_data = json.load(file)

        return class_data["students"]

    def completedDay(self, cls_id : int , year : int , data : list):

        # get the class
        csv_file_name = f"{year}@{cls_id}@class_register.csv"
        # create the csv writer
        dialect = csv.get_dialect("unix")
        writer = csv.writer(open(os.path.join(class_root_path, csv_file_name), "a"), dialect= dialect)
        # write the data
        date = QDate.currentDate().toString("yyyy:mm:dd")

        for item in data:
            id = item[0]
            state = item[1]
            writer.writerow([date, id, state])

        writer.writerow([None, None, None])

        # update the json file for class hostory
        history_file = f"{year}@{cls_id}@classhistory.json"
        with open(os.path.join("db/classes_history", history_file)) as file:
            history = json.load(file)

        # add the today to the class
        history.append((QDate.currentDate().toString("yyyy:mm:dd"), True))
        with open(os.path.join("db/classes_history", history_file) ,"w") as file:
            json.dump(history, file, indent=4)


