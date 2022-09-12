import Log
import sqlite3
from os import getcwd
from pathlib import Path
from sqlite3 import OperationalError

class SQLite:

    def __init__(self):

        self.Path = Path(getcwd() + '/Data/Database/database.db')

        self.log = Log.Generate()
        self.conn = sqlite3.connect(self.Path)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, columns))
        self.conn.commit()

    def insert_data(self, table_name, columns, data):

        try:

            data = ', '.join(["'"+value+"'" for value in data])
            columns = ', '.join([column for column in columns])

            Query = f"INSERT INTO {table_name} ({columns}) VALUES ({data}) "

            self.cursor.execute(Query)
            self.conn.commit()

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        except OperationalError as error:
            self.log.Write("Database.py | OperationalError # " + str(error))
            return False
        except Exception as error:
            self.log.Write("Database.py | GeneriError # " + str(error))
            return False


    def select_data(self, table_name, columns, where = None):

        try:

            columns = ', '.join([column for column in columns])

            if where is None:
                Query = f"SELECT {columns} FROM {table_name}"
            else:
                Query = f"SELECT {columns} FROM {table_name} WHERE {where}"

            self.cursor.execute(Query)

            rows = self.cursor.fetchall()

            # Convert tuple to list
            data = [list(row) for row in rows]

            return data
        except OperationalError as error:
            self.log.Write("Database.py | OperationalError # " + str(error))

    def update_data(self, table_name, data, where):

        where = ''.join([f"{column} = '{value}'" for column, value in where.items()])
        data = ', '.join([f"{column} = '{value}'" for column, value in data.items()])

        self.cursor.execute(f"UPDATE {table_name} SET {data} WHERE {where}")
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def delete_data(self, table_name, data):

        where = ''.join([f"{column} = '{value}'" for column, value in data.items()])

        self.cursor.execute("DELETE FROM {} WHERE {}".format(table_name, where))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def custom_query(self, query):

        self.cursor.execute(query)

        return self.cursor.fetchall()