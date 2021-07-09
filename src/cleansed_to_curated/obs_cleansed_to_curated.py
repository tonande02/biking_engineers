import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

def connect_db(): # returns the connection and the cursor to the connection
    conn = psycopg2.connect(
        host = "academy-de-course-2021-summer-prod-001.postgres.database.azure.com",
        dbname = "biking_test",
        user = "consultant@academy-de-course-2021-summer-prod-001",
        password = "3eBXkuVvaJ5ncNGP",
        port = 5432
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    return conn, cur

def disconnect_db(cur, conn):
    cur.close()
    conn.close()

def db_ex(cur, conn, ex_string):
    cur.execute(ex_string)
    conn.commit()

def db_ex_pr(cur, ex_string):
    cur.execute(ex_string)
    print(cur.fetchall())

def create_table(cur):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS python_table (id SERIAL PRIMARY KEY, name TEXT, description TEXT, updated TIMESTAMP);"
        )

def insert_db(cur, name, description = None): # return the number of rows inserted into the database
    if description == None: description = str(name + " description")
    values = (name, description, datetime.now())
    cur.execute("INSERT INTO python_table (name, description, updated) VALUES (%s, %s, %s);", values)
    return cur.rowcount

def insert_many(cur, in_records): # name, description = None): # return the number of rows inserted into the database
    records = []
    for item in in_records:
        if item[0] == None:
            name = None
        else:
            name = item[0]
        if item[1] == None:
            desc = str(item[0] + " description")
        else:
            desc = item[1]
        records.append((name, desc, datetime.now()))
    cur.executemany("INSERT INTO python_table (name, description, updated) VALUES (%s, %s, %s);", records)
    return cur.rowcount

def update_db(cur, iid, record): # return 0 if the row is not present in the database. Else return 1.
    id = str(iid)
    cur.execute(f"SELECT * FROM python_table WHERE id = {id};")
    print(id)
    result = cur.fetchone() # how to return number of rows???
    if cur.rowcount:
        if record[0] == None: name = result[0][1]
        else: name = record[0]
        if record[1] == None: description = result[0][2]
        else: description = record[1]
        values = (name, description, datetime.now(), id)
        cur.execute("UPDATE python_table SET name = %s, description = %s, updated = %s WHERE id = %s;", values)
    return cur.rowcount

def del_row(cur, iid):
    id = str(iid)
    cur.execute(f"DELETE FROM python_table WHERE id = {id};")
    return cur.rowcount


def main():
    connection, cursor = connect_db()
#    create_table(cursor)
#    print("insert: ", insert_db(cursor, "433n63lksg", "the1 desc yeah"))
#    print("insertmany: ", insert_many(cursor, [("1mJust1", "j 1 m111"), ("2mJust1", "2j 1 m111"), ("3mJust1", "3j 1 m111"), ("4mJust1", "44j 1 msa111")]))
#    print("update: ", update_db(cursor, 40, ("y40", "id 9 ok")))
#    print("del_row: " + str(del_row(cursor, 41)))
    
    disconnect_db(cursor, connection)

if __name__ == "__main__":
    main()

"""
    try:
    except Exception as e:
        print(e)
    else:
    finally:


# ---------------------------------------------------
def create_db(connection, cursor):
    conn = connection
    cur = cursor
    cur.execute("CREATE TABLE IF NOT EXISTS python_table (id SERIAL PRIMARY KEY, name TEXT, description TEXT, updated TIMESTAMP);")
    conn.commit()






def create_tables():
    commands = (
        CREATE TABLE python_table (
            id INT PRIMARY KEY,
            name TEXT,
            description text,
            updated datetime
        )
    )


cur.execute("SELECT * FROM test;")
result = cur.fetchall()
result


cur.mogrify("SELECT %s, %s, %s, %s, %s;", (None, True, False, 1, 1.0))
"""