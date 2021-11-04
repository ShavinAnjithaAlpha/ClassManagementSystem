import sqlite3

class DBManager:
    def __init__(self, db_file : str, save_config  = True):
        self.db_file = db_file
        self.save_config = save_config

    def __enter__(self):
        #create the connection and return it
        self.connect = sqlite3.connect(self.db_file)

        return self.connect.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.save_config:
            self.connect.commit()

        self.connect.close()
        del self