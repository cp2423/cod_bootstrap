from database.cwgc import Database

db = Database()
res = db.find("745394")
print(res)