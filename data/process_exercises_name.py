import json

data = json.load(open("mongo_ready_exercises.json",encoding="utf8"))
ndata = []
for d in data:
    d["name"] = d["name"].lower()
    ndata.append(d)
fhand = open("mongo_ready_exercises_lower.json","w")
json.dump(ndata, fhand)
fhand.close()