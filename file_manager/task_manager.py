import json
import os, shutil

import json5
from PyQt5.QtCore import QDate, QTime

class TaskManger:

    path = "db\\tasks\\data"
    file_path = "db\\tasks\\files"

    @staticmethod
    def addNewtask(title, end_date, end_time, **kwargs):

        # get the current date
        current_date = QDate.currentDate()
        task = {
            "title" : title,
            "date" : current_date.toString("yyyy MMM dd"),
            "end_date" : end_date.toString("yyyy MMM dd"),
            "end_time" : end_time.toString("hh:mm A"),
            "is_completed" : False
        }

        if kwargs.get("sub_tasks", False):
            data = kwargs["sub_tasks"]
            task["sub_tasks"] = [(i, False) for i in data]

        if kwargs.get("images", False):
            files = kwargs["images"]
            new_files = []
            # copy the files to the images folder
            for img in files:
                _ , name = os.path.split(img)
                new_path = os.path.join(TaskManger.file_path , name)
                shutil.copyfile(img , new_path)
                new_files.append(new_path)

            task["images"] = new_files

        if kwargs.get("des", False):
            task["des"] = kwargs.get("des")

        if (os.path.exists(os.path.join(TaskManger.path , f"task_{current_date.year()}_{current_date.month()}.json"))):
            with open(os.path.join(TaskManger.path , f"task_{current_date.year()}_{current_date.month()}.json")) as file:
                data = json5.load(file)
                data.append(task)

        else:
            # create the new json file
            data = [task, ]

        with open(os.path.join(TaskManger.path , f"task_{current_date.year()}_{current_date.month()}.json"), "w") as file:
            json5.dump(data, file, indent=4)

    @staticmethod
    def getTasksForMonth(year : int , month : int):

        # open the files
        if not os.path.exists(os.path.join(TaskManger.path , f"task_{year}_{month}.json")):
            raise FileNotFoundError

        with open(os.path.join(TaskManger.path , f"task_{year}_{month}.json")) as file:
            data = json5.load(file)

        # return the task list
        return data

    @staticmethod
    def setAsComplete(title, date : QDate, status = True):

        data = []
        # open the json file
        with open(os.path.join(TaskManger.path , f"task_{date.year()}_{date.month()}.json")) as file:
            data = json5.load(file)

            # refresh the task as complete
            for task in data:
                if task["title"] == title and task["date"] == date.toString("yyyy MMM dd"):
                    task["is_completed"] = status

        # save the file
        with open(os.path.join(TaskManger.path , f"task_{date.year()}_{date.month()}.json"), "w") as file:
            json5.dump(data , file, indent=4)

    @staticmethod
    def deleteTask(title , date):

        d = QDate.fromString(date, "yyyy MMM dd")
        # open the json file
        with open(os.path.join(TaskManger.path ,f"task_{d.year()}_{d.month()}.json")) as file:
            data = json5.load(file)

        new_data = []
        for item in data:
            if item["title"] == title and item["date"] == date:
                continue
            new_data.append(item)

        # save the file
        with open(os.path.join(TaskManger.path ,f"task_{d.year()}_{d.month()}.json") ,"w") as file:
            json5.dump(new_data, file, indent=4)

