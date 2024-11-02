from bs4 import BeautifulSoup
from database.db import Database

data = []

with open("database/baclac_table.html") as f:
    soup = BeautifulSoup(f, 'html.parser')

for row in soup.findAll("tr")[1:]:
    head = row.th.text
    # hack for one line where to is To
    head = head.replace("To", "to")
    first, last = head.split(" to ")
    cells = row.findAll("td")
    vol = cells[1].text
    data.append({
        "vol": vol,
        "first": first,
        "last": last
    })

db = Database()
with db.con as con:
    cur = con.execute("CREATE TABLE volumes(vol, first, last)")
    cur.executemany("INSERT INTO volumes VALUES(:vol, :first, :last)", data)
