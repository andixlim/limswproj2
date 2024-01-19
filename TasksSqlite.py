'''
This is the interface to an SQLite Database
'''

import sqlite3
import json
import tkinter
from tkinter import filedialog

class TaskSqlite:
    def __init__(self, dbName='Tasks.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.json = self.dbName.replace(".db", ".json")
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tasks (
                Task Num TEXT PRIMARY KEY,
                Assignment TEXT,
                Status TEXT,
                Due Date TEXT,
                Subject TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Tasks (
                Task_Num TEXT PRIMARY KEY,
                Assignment TEXT,
                Status TEXT,
                Due Date TEXT,
                Subject TEXT)''')
        self.commit_close()

    def tasklist(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Task Num')
        tasks =self.cursor.fetchall()
        self.conn.close()
        return tasks

    def insert_task(self, task_num, assignment, status, due, subject):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Tasks (task_num, assignment, status, due, subject) VALUES (?, ?, ?, ?, ?)',
                    (task_num, assignment, status, due, subject))
        self.commit_close()

    def remove_task(self, task_num):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Tasks WHERE id = ?', (task_num,))
        self.commit_close()

    def update_task(self, new_assignment, new_status, new_due, new_subject, task_num):
        self.connect_cursor()
        self.cursor.execute('UPDATE Task SET assignment = ?, status = ?, due = ?, subject = ? WHERE id = ?',
                    (new_assignment, new_status, new_due, new_subject, task_num))
        self.commit_close()

    def task_exists(self, task_num):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Tasks WHERE id = ?', (task_num,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as f:
            taskentries = self.tasklist()
            for entry in taskentries:
                print(entry)
                f.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

    def import_csv(self):
        csvfile = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Choose a csv file to import into the database.")
        with open(csvfile, "r") as f:
            readfile = f.readlines()
            for line in readfile:
                info = line.strip().split(",")
                self.insert_task(info[0], info[1], info[2], info[3], info[4])

    
    def export_json(self):
        taskentries = {}
        x = 0
        with open(self.json, "w") as file:
            for task in self.tasks:
                task = [task.task_num, task.assignment, task.status, task.duedate, task.subject]
                x += 1
                taskentries[f"task " + str(x)] = task
            jsonentries = json.dumps(taskentries)
            file.write(jsonentries)

def test_EmpDb():
    itask = TaskSqlite(dbName='TasksSql.db')

    for entry in range(30):
        itask.insert_task(entry, f'Assignment{entry} status{entry}', f'Due date {entry}', 'Math')
        assert itask.task_exists(entry)

    all_entries = itask.tasklist()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        itask.update_task(f'Assignment{entry} status{entry}', f'Due date {entry}', 'Physics', entry)
        assert itask.task_exists(entry)

    all_entries = itask.tasklist()
    assert len(all_entries) == 30

    for entry in range(10):
        itask.remove_task(entry)
        assert not itask.task_exists(entry) 

    all_entries = itask.tasklist()
    assert len(all_entries) == 20