import sqlite3

# connect to db
con = sqlite3.connect("vineyards/db.sqlite3")
cur = con.cursor()

# read data from file
f = open('coordinates.txt', 'r')
cont = f.read()
f.close()

# read data from file
f = open('names_normalized.txt', 'r')
names = f.read()
f.close()

names_list = names.split("\n")
print(names_list)

# format for inserting to db
rows = cont.split('\n')
rows = rows[1:-1]  # delete first row with captions
formatted = [(x.split(';')[1], x.split(';')[0]) for x in rows]
print(formatted)
result = []

for i in range(len(formatted)):
    result += [(*formatted[i], names_list[i])]

print(result)

# insert into db
cur.executemany("INSERT INTO forecasts_existingvineyard (x, y, name) VALUES (?, ?, ?)", result)
con.commit()
con.close()
