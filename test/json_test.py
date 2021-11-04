import json

# create the simple json file
data = ["shavin", "resani", "kasun", "pytha"]
new_data = ["himeth", "randika"]

with open("simple.json", "a") as file:
    json.dump(new_data, file, indent=4)