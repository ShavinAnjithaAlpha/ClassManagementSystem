import csv

writer = csv.DictWriter(open("sample2.csv", "w"), fieldnames=["Name", "age"])
writer.writeheader()

writer.writerow({"Name" : "shavin", "age" : 19})