import json
import sqlite3

data = {}
data["players"] = []
data["players"].append({"level":1,"user":"Joaco","score":100})
data["players"].append({"level":2,"user":"Nico","score":200})
data["players"].append({"level":3,"user":"Vicen","score":300})

with open("players.json","w") as file:
    json.dump(data,file,indent=2)

with sqlite3.connect("players_database.db") as connection:
    try:
        statement = '''
                    create table Players
                    (
                        level integer,
                        user text,
                        score text
                    )
                    '''
        connection.execute(statement)
    except:
        print("Error")
