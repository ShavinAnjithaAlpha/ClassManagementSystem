import csv


data = [["data" ,"shaj", "gjhhdg"],
        ["sjjd", "ghdf", "jfjf"]]


with open("sample.csv", "a") as file:
        # file.seek(0)
        dl  = csv.get_dialect("unix")
        writer = csv.writer(file, dialect=dl)
        dialect = csv.list_dialects()
        print(dialect)
        writer.writerows(data)

reader = csv.reader(open("sample.csv"))
for i in reader:
        print(i)
