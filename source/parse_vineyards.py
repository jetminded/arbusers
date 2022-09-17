import random
import sqlite3

# connect to db
con = sqlite3.connect("vineyards/db.sqlite3")
cur = con.cursor()

# read data from file
f = open('coordinates.txt', 'r')
cont = f.read()
f.close()

# read names from file
f = open('names_normalized.txt', 'r')
names = f.read()
f.close()

names_list = names.split("\n")

# read data absolute from file
f = open('VINEYARDS.TXT', 'r')
abs = f.read()
f.close()


grapes_list = ['Саперави', 'Ркацетели', 'Совиньон Блан', 'Красностоп']

# format for inserting to db
rows = cont.split('\n')
rows = rows[1:-1]  # delete first row with captions
formatted = [(x.split(';')[1], x.split(';')[0]) for x in rows]

# format abs for inserting to db
rows_abs = abs.split('\n')
rows_abs = rows_abs[1:-1]  # delete first row with captions
formatted_abs = [tuple(x.split()[1:]) for x in rows_abs]

result = []
for i in range(len(formatted)):
    result += [(*formatted[i], *formatted_abs[i], names_list[i], grapes_list[random.randint(0, 3)])]

print(result)

# insert into db
cur.executemany("INSERT INTO forecasts_existingvineyard (x, y, x_abs, y_abs, name, grape) VALUES (?, ?, ?, ?, ?, ?)", result)
con.commit()
con.close()
