import sqlite3

from PyQt5.QtCore import QDate

db_file = "db/main.db"
SEX = {"male" : 0, "female" : 1, "other" : 2}

class DBManager:
    def __init__(self, db_file : str, save_config  = True):
        self.db_file = db_file
        self.save_config = save_config

    def __enter__(self):
        #create the connection and return it
        self.connect = sqlite3.connect(self.db_file)

        return self.connect.cursor()

    def __exit__(self):

        if self.save_config:
            self.connect.commit()

        self.connect.close()
        del self

class StudentManager:

    param = {
        ["firstName", "fName", "firstname", "first_name", "FirstName"] : "firstName",
        ["lastName", "lName", "lastname", "last_name", "LastName"] : "lastName",
        ["address", "Address", "adr", "Adr"] : "address",
        ["sex", "Sex", "sexual"] : "sex",
        ["telNum", "num", "TelNum", "telephoneNumber", "telephone_number"] : "telNumber",
        ["parTelNum", "parNum", "parMobNum", "parent_mobile_number", "parentMobileNumber"] : "parTelNum",
        ["id", "index", "Index", "i"] : "id",
        ["bDay", "birthDay", "birth_day", "birthday", "BirthDay"] : "birthDay",
        ["eDay", "enteredDay", "enterDay", "enter_day", "entered_day" , "eday"] : "enteredDay"
    }

    @staticmethod
    def getKey(text : str):
        for key in StudentManager.param.keys():
            if (text in key):
                return StudentManager.param.get(key)

        return None


    def initiateTable(self):

       with DBManager(db_file) as cursor:
           # create the table with specific rows
           cursor.execute("""CREATE TABLE student_table(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                                              firstName TEXT NOT NULL,
                                                              lastName TEXT NOT NULL,
                                                              address TEXT NOT NULL,
                                                              telNumber TEXT,
                                                              parTelNumber TEXT NOT NULL,
                                                              birthDay TEXT NOT NULL,
                                                              enteredDay TEXT NOT NULL,
                                                              sex INTEGER NOT NULL)""")

    def addStudent(self, details : dict):
        # create the connection and
        with DBManager(db_file) as cursor:
            # getthe data from the ditionary
            fName , lName = details["firstName"], details["lastName"]
            add = details["address"]
            num , parNum = details.get("telNumber" , None) , details["parTelNumber"]
            bday = details["birthDay"]
            sex = SEX.get(details["sex"], 2)

            eday = QDate().currentDate().toString("yyyy MM dd")

            cursor.execute(f""" INSERT INTO student_table(firstName, lastName, address, telNumber , 
                                                                    parTelNumber , birthDay, enteredDay, sex)
                                VALUES('{fName}', '{lName}', '{add}', '{num}', '{parNum}', '{bday}', '{eday}', {sex})""")

    def addStudents(self, detail_list : list[dict]):
            with DBManager(db_file) as cursor:
                for details in detail_list:
                    # get the data from the ditionary
                    fName, lName = details["firstName"], details["lastName"]
                    add = details["address"]
                    num, parNum = details.get("telNumber", None), details["parTelNumber"]
                    bday = details["birthDay"]
                    sex = SEX.get(details["sex"], 2)

                    eday = QDate().currentDate().toString("yyyy MM dd")

                    cursor.execute(f""" INSERT INTO student_table(firstName, lastName, address, telNumber , 
                                                                                       parTelNumber , birthDay, enteredDay, sex)
                                                   VALUES('{fName}', '{lName}', '{add}', '{num}', '{parNum}', '{bday}', '{eday}', {sex})""")


    def get(self, index : int , key  : str):
        key = StudentManager.getKey(key)

        if key:
            with DBManager(db_file ,False) as cursor:
                try:
                    cursor.execute(f""" SELECT {key} FROM student_table WHERE id = {index} """)
                    return cursor.fetchall()[0][0]
                except:
                    raise IndexError()
        else:
            return None

    def get(self, indexes : list[int] , key  :str):
        key = StudentManager.getKey(key)

        data = []
        if key:
            with DBManager(db_file, False) as cursor:
                for id in indexes:
                    try:
                        cursor.execute(f""" SELECT {key} FROM student_table WHERE id = {id} """)
                        data.append(cursor.fetchall()[0][0])
                    except:
                        data.append(-1)

        return data

    def get(self, key : str):
        key = StudentManager.getKey(key)
        if key:
            with DBManager(db_file, False) as cursor:
                cursor.execute(f"""SELECT {key} FROM student_table """)
                data = [item[0] for item in cursor.fetchall()]
        else:
            data = None

        return data

    def get(self, index : int):
        with DBManager(db_file, False) as cursor:
            try:
                cursor.execute(f"""SELECT * FROM student_table WHERE id = {index} """)
                data = cursor.fetchall()[0]
            except:
                data = None

        return data

    def set(self, index : int , key : str , new_value : str):
        key = StudentManager.getKey(key)
        if key:
            with DBManager(db_file) as cursor:
                try:
                    if (key != "id" and key != "sex"):
                        cursor.execute(f"""UPDATE student_table SET {key} = '{new_value}' WHERE id = {index} """)
                    else:
                        raise PermissionError()
                except:
                    raise IndexError()
        else:
            raise KeyError()

    def delete(self, index : int):

        with DBManager(db_file) as cursor:
            try:
                cursor.execute(f"""DELETE FROM student_table WHERE id = {index} """)
            except:
                raise IndexError()

    def getID(self, key1 , value1 , key2, value2) -> int:

        key1 = StudentManager.getKey(key1)
        key2 = StudentManager.getKey(key2)

        if key1 and key2:
            with DBManager(db_file) as cursor:
                try:
                    cursor.execute(f"""SELECT id FROM student_table WHERE {key1} = '{value1}' AND {key2} = '{value2}' """)
                    return cursor.fetchall()[0][0]
                except:
                    raise KeyError
        else:
            return None