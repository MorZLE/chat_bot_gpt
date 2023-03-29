import sqlite3


class DB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def con_db_app(self):
        self.connection = sqlite3.connect('chyrik.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS USER (ID text, data text,time text);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS BAN (name text,time text);')
        self.connection.commit()

    def exec(self, query, *args):
        """Функция отправки запроса"""
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            result = self.cursor.fetchall()
            return result, self.cursor.description
        except TypeError as te:
            print(te)
          
        except (sqlite3.OperationalError,UnboundLocalError) as err:
            if 'no results to fetch' in str(err):
                print('Нету данных для вывода!')
            else:
                print(err)


