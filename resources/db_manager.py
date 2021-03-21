import sqlite3
import os

#VARS
src_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(os.path.dirname(src_path), "resources")


"""CREATE DB:
try:
    sqliteConnection = sqlite3.connect(os.path.join(resources_path, 'SQLite_Python.db'))
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("The SQLite connection is closed")
"""

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = os.path.join(resources_path, 'SQLite_Python.db')

    sql_create_police_events_table = """CREATE TABLE IF NOT EXISTS police_events (
                                    Id integer PRIMARY KEY,
                                    Name text NOT NULL,
                                    Summary text,
                                    Type text NOT NULL,
                                    Datetime text NOT NULL,
                                    Gps text NOT NULL,
                                    Location text NOT NULL
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_police_events_table)
        print ("Table created!")

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()