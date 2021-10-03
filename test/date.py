from PyQt5.QtCore import QDate, QTime, QDateTime

DAYS = ["Monday", "TuesDay", "Wednesday", "ThursDay", "FriDay", "SaturDay", "SunDay"]

date = QDate(2021, 10, 3)
print(date.toString("yyyy MMM dd"))

print(DAYS[date.dayOfWeek() - 1])

# print(date.addDays(7))
date = date.addDays(7)
print(date.toString("yyyy MMM dd"))

print(DAYS[date.dayOfWeek() - 1])

print(date.endOfDay())

print(date > QDate(2022, 4, 5))

# create the date time object
datetime = QDateTime(date)
print(datetime.toString("yyyy MMM dd | hh:mm:ss"))
print(datetime.timeZone().comment())

# create the time object
time = QTime(2, 40, 55)
time2 = QTime(5, 44, 44)

print(time < time2)