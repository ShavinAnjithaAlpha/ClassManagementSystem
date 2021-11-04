import os
import time

class Logger:
    def __init__(self, file_name : str):
        self.file = file_name
        self.query_pack = []

        with open(self.file, "w") as file:
            file.write("start")

    def CHANGED(self, message):
        current_time = time.strftime("%D %H:%M")

        self.query_pack.append(f"[CHANGED] {current_time} | {message}\n")
        if len(self.query_pack) >= 10:
            self.save()

    def DISPLAY(self, message):

        current_time = time.strftime("%d %H:%M")
        self.query_pack.append(f"[DISPLAY] {current_time} | {message}\n")

        if len(self.query_pack) >= 10:
            self.save()

    def save(self):

        with open(self.file, "a") as file:
            for query in self.query_pack:
                file.write(query)

        self.query_pack = []

    def close(self):

        self.save()

