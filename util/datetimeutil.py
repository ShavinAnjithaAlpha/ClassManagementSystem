from PyQt5.QtCore import QDate, QTime, QDateTime

class DateTimeUtil:

    # create the additional static method for utility
    @staticmethod
    def isCrash(ex_time1 : QTime, ex_time2 : QTime , new_time1 : QTime , new_time2 : QTime):
        min_time = min(ex_time1, ex_time2)
        max_time = max(ex_time1, ex_time2)

        new_min = min(new_time1, new_time2)
        new_max = max(new_time1, new_time2)

        if (new_max < max_time and new_max > min_time):
            return True
        if (new_min > min_time and new_min < max_time):
            return True

    @staticmethod
    def gradeFromText(date : str):

        y, m, d = date.split("-")
        date = QDate(int(y), int(m), int(d))

        diff = QDate().currentDate().year() - date.year() -  6

        if int(m) == 1:
            diff += 1

        if diff == 14:
            return diff - 1
        return diff

    @staticmethod
    def grade(date : QDate):

        diff = QDate().currentDate().year() - date.year() - 6

        if date.month() == 1:
            diff += 1

        if diff == 14:
            return diff - 1
        return diff

