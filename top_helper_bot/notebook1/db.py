import os
import sqlite3
from .classes_new import Note
from prettytable import from_db_cursor
from abc import abstractmethod, ABC

class Database():
    def __init__(self ):
        if os.path.exists('notes') == False:
            os.mkdir('notes')
        self.connection = sqlite3.connect('.//notes//notes.db')
        self.cur = self.connection.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS notes(
                   note_id INTEGER PRIMARY KEY,
                   tag TEXT,
                   name TEXT,
                   created TEXT,
                   changed TEXT);
                """)
        self.connection.commit()

    def execute(self, sql, params):
        try:
            with self.connection:
                self.cur.execute(sql, params)
        except:
            raise f"Error creating attribute"

    def add_record(self, note: Note):
        sql = "INSERT INTO notes (name, created) VALUES (?,?)"
        params = (note.name, note.created)
        self.execute(sql, params)


    def change_record(self, note):
        sql = "UPDATE notes SET changed = ? WHERE name = ?"
        params = (note.changed, note.name)
        self.execute(sql, params)

    def remove_record(self, note):
        sql = "DELETE FROM  notes WHERE name = ?;"
        params = (note.name)
        self.execute(sql, params)

    def add_tag(self, note):
        note.change_tag()
        sql = "UPDATE notes SET tag = ? WHERE name = ?);"
        params = (note.tag, note.name)
        self.execute(sql, params)

    def remove_tag(self, note):
        note.remove_tag()
        sql = "UPDATE notes SET tag = ? WHERE name = ?);"
        params = (note.tag, note.name)
        self.execute(sql, params)

    def check_name(self, name):
        sql = 'SELECT COUNT (*) FROM notes WHERE name = ?'
        params = (name,)
        print(self.execute(sql, params))
        return self.execute(sql, params)

class Table(ABC):
    @abstractmethod
    def print_table(self, db: Database):
        pass
    @abstractmethod
    def show_all(self, db: Database):
        pass

    @abstractmethod
    def sort(self, db: Database):
        pass

    @abstractmethod
    def filter(self, db: Database, tag):
        pass

class Notes_table(Table):

    def print_table(self, db: Database, sql, params):
        db.execute(sql, params)
        table = from_db_cursor(db.cur)
        print(table)

    def show_all(self, db: Database):
        sql = "SELECT * FROM notes"
        params = ()
        self.print_table(db, sql, params)

    def sort(self, db: Database):
        sql = "SELECT name, created, changed FROM notes ORDER BY created;"
        params = ('',)
        self.print_table(db, sql, params)

    def filter(self, db: Database, tag):
        sql = "SELECT name, created, changed FROM notes WHERE tag=?"
        params = (tag,)
        self.print_table(db, sql, params)

db = Database()
table = Notes_table()