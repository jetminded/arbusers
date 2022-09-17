import sqlite3

# connect to db
con = sqlite3.connect("vineyards/db.sqlite3")
cur = con.cursor()

# read data from file
f = open('VINEYARDS.TXT', 'r')
cont = f.read()
f.close()

# format for inserting to db
rows = cont.split('\n')
rows = rows[1:-1]  # delete first row with captions
formatted = [tuple(x.split()[1:]) for x in rows]
# formatted = [(*row, "") for row in formatted]
print(formatted)

# insert into db
cur.executemany("INSERT INTO forecasts_existingvineyard (x, y, name) VALUES (?, ?, '')", formatted)
con.commit()
con.close()
