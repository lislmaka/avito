import sqlite3
import os
import datetime

db_url = os.environ.get("AVITO_DB_FULLPATH_2")


def sqlite3_get_fields_names():
    connection = sqlite3.connect(db_url)
    cursor = connection.cursor()

    # Выбираем всех пользователей
    cursor.execute("SELECT name FROM PRAGMA_TABLE_INFO('avito')")
    fields = cursor.fetchall()

    connection.close()

    return [i[0] for i in fields]


def sqlite3_add_new_field(field_name):
    connection = sqlite3.connect(db_url)
    cursor = connection.cursor()

    cursor.execute(
        f"""
    ALTER TABLE avito 
    ADD COLUMN {field_name} 'TEXT'
    """
    )

    connection.close()


def sqlite3_check_if_exist(id):
    connection = sqlite3.connect(db_url)
    cursor = connection.cursor()

    id = cursor.execute("SELECT id FROM avito WHERE id=?", (id,)).fetchone()

    connection.commit()
    connection.close()

    return bool(id)


def sqlite3_add_new_values(my_dict):
    connection = sqlite3.connect(db_url)
    cursor = connection.cursor()

    if not sqlite3_check_if_exist(my_dict["id"]):
        if "date_update" in my_dict:
            del my_dict["date_update"]
        my_dict["date_add"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        columns = ", ".join(my_dict.keys())
        placeholders = ", ".join("?" * len(my_dict))
        sql = "INSERT INTO avito ({}) VALUES ({})".format(columns, placeholders)
        cursor.execute(sql, tuple(my_dict.values()))

        connection.commit()
        status = "insert"
    else:
        if "date_add" in my_dict:
            del my_dict["date_add"]
        if "status" in my_dict:
            del my_dict["status"]
            
        my_dict["date_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        my_dict = {k: v for k, v in my_dict.items() if v}
        columns = ", ".join([f"{k} = ?" for k in my_dict.keys()])
        values = list(my_dict.values())
        values.append(my_dict["id"])
        sql = f"UPDATE avito SET {columns} WHERE id = ?"
        cursor.execute(sql, values)
        connection.commit()
        status = "update"

    connection.close()

    return status
