import sqlite3

from PyQt5.QtCore import QDate
from file_manager.db_manager import DBManager

db_file = "db/main.db"
SEX = {"male" : 0, "female" : 1, "other" : 2}

class StudentManager:

    param = {
        "firstName" : ["firstName", "fName", "firstname", "first_name", "FirstName"],
        "lastName" : ["lastName", "lName", "lastname", "last_name", "LastName"],
        "address" : ["address", "Address", "adr", "Adr"],
        "sex" : ["sex", "Sex", "sexual"],
        "telNumber" : ["telNum", "num", "TelNum", "telephoneNumber", "telephone_number"],
        "parTelNumber" : ["parTelNum", "parNum", "parMobNum", "parent_mobile_number", "parentMobileNumber"],
        "id" : ["id", "index", "Index", "i", "ID"],
        "birthDay" : ["bDay", "birthDay", "birth_day", "birthday", "BirthDay"],
        "enteredDay" : ["eDay", "enteredDay", "enterDay", "enter_day", "entered_day" , "eday"],
        "school" : ["school", "School", "sch", "Sch"]
    }

    @staticmethod
    def getKey(text : str):
        for key in StudentManager.param.keys():
            if (text in StudentManager.param.get(key)):
                return key

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
                                                              school TEXT NOT NULL,
                                                              enteredDay TEXT NOT NULL,
                                                              sex INTEGER NOT NULL)""")

    def addStudent(self, details : dict):
        # create the connection and
        with DBManager(db_file) as cursor:
            # get the data from the ditionary
            fName , lName = details["firstName"], details["lastName"]
            add = details["address"]
            num , parNum = details.get("telNumber" , None) , details["parTelNumber"]
            bday = details["birthDay"]
            sex = SEX.get(details["sex"], 2)
            school = details["school"]

            eday = QDate().currentDate().toString("yyyy MM dd")

            cursor.execute(f""" INSERT INTO student_table(firstName, lastName, address, telNumber , 
                                                                    parTelNumber , birthDay, school ,enteredDay, sex)
                                VALUES('{fName}', '{lName}', '{add}', '{num}', '{parNum}', '{bday}', '{school}' ,'{eday}', {sex})""")

    def addStudents(self, detail_list : list[dict]):
            with DBManager(db_file) as cursor:
                for details in detail_list:
                    # get the data from the dictionary
                    fName, lName = details["firstName"], details["lastName"]
                    add = details["address"]
                    num, parNum = details.get("telNumber", None), details["parTelNumber"]
                    bday = details["birthDay"]
                    sex = SEX.get(details["sex"], 2)
                    school = details["school"]

                    eday = QDate().currentDate().toString("yyyy MM dd")

                    cursor.execute(f""" INSERT INTO student_table(firstName, lastName, address, telNumber , 
                                                                parTelNumber , birthDay, enteredDay, sex)
                                    VALUES('{fName}', '{lName}', '{add}', '{num}', '{parNum}', '{bday}', '{school}' , '{eday}', {sex})""")


    def get(self, index : int , key : str):
        key_ = StudentManager.getKey(key)

        if key_:
            with DBManager(db_file ,False) as cursor:
                try:
                    cursor.execute(f""" SELECT {key_} FROM student_table WHERE id = {index} """)
                    return cursor.fetchall()[0][0]
                except:
                    raise IndexError()
        else:
            return None

    def gets(self, indexes : list[int] , key  :str):
        key_ = StudentManager.getKey(key)

        data = []
        if key_:
            with DBManager(db_file, False) as cursor:
                for id in indexes:
                    try:
                        cursor.execute(f""" SELECT {key_} FROM student_table WHERE id = {id} """)
                        data.append(cursor.fetchall()[0][0])
                    except:
                        data.append(-1)

        return data

    def getFromKey(self, key : str):
        key_ = StudentManager.getKey(key)
        if key_:
            with DBManager(db_file, False) as cursor:
                cursor.execute(f"""SELECT {key_} FROM student_table """)
                data = [item[0] for item in cursor.fetchall()]
        else:
            data = None

        return data

    def getFromIndex(self, index : int):
        with DBManager(db_file, False) as cursor:
            try:
                cursor.execute(f"""SELECT * FROM student_table WHERE id = {index} """)
                data = cursor.fetchall()[0]
            except:
                data = None

        return data

    def set(self, index : int , key : str , new_value : str):
        key_ = StudentManager.getKey(key)
        if key_:
            with DBManager(db_file) as cursor:
                try:
                    if (key_ != "id" and key_ != "sex"):
                        cursor.execute(f"""UPDATE student_table SET {key_} = '{new_value}' WHERE id = {index} """)
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

        key1_ = StudentManager.getKey(key1)
        key2_ = StudentManager.getKey(key2)

        if key1_ and key2_:
            with DBManager(db_file) as cursor:
                try:
                    cursor.execute(f"""SELECT id FROM student_table WHERE {key1_} = '{value1}' AND {key2_} = '{value2}' """)
                    return cursor.fetchall()[0][0]
                except:
                    raise KeyError
        else:
            return None