import csv
import re
import sys
import sqlite3
import os

def make_new_data(data):
    d = {}

    for key in data:
        d.setdefault(data[key]["db_key"], data[key]["db_val"])

    return d

def sqlite_update(id, data):
    db_url = os.environ.get("AVITO_DB_FULLPATH_2")
    connection = sqlite3.connect(db_url)
    cursor = connection.cursor()   

    columns = ", ".join([f"{k} = ?" for k in data.keys()])
    values = list(data.values())
    values.append(id)
    sql = f"UPDATE avito SET {columns} WHERE id = ?"
    cursor.execute(sql, values)
    connection.commit()

    connection.close()

if len(sys.argv) == 2:
    id = sys.argv[1]
else:
    print("Укажите id")
    exit()

filename = "distances_objects/загруженное.csv"  # File name
fields = []  # Column names
rows = []  # Data rows

with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)  # Reader object

    fields = next(csvreader)  # Read header
    for row in csvreader:  # Read rows
        rows.append(row)

    print("Total no. of rows: %d" % csvreader.line_num)  # Row count

data = {
    "Аптека": {"db_key": "to_apteka", "db_val": ""},
    "Почт": {"db_key": "to_pochta", "db_val": ""},
    "Сбербанк": {"db_key": "to_bank", "db_val": ""},
    "Поликлиника": {"db_key": "to_bolnitsa", "db_val": ""},
    "Магнит": {"db_key": "to_magnit", "db_val": ""},
    "рочка": {"db_key": "to_pyaterochka", "db_val": ""},
    "Ozon": {"db_key": "to_ozon", "db_val": ""},
    "Wildberries": {"db_key": "to_wildberries", "db_val": ""},
}
for row in rows:
    for key in data:
        if key.lower() in row[0].lower():
            data[key]["db_val"] = re.sub(r"[^\d]", "", row[-1])

data = make_new_data(data)
print(data)
sqlite_update(id, data)
