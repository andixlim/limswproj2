from TaskEntry import TaskEntry
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter
import json

class Tasks:
    def __init__(self, init=False, dbName='Tasks.csv'):
        # CSV filename         
        self.dbName = dbName
        self.json = dbName.replace(".csv", ".json")
        # initialize container of database entries
        self.tasks = []

    def tasklist(self):
        tupleList = [(entry.task_num, entry.assignment, entry.status, entry.duedate, entry.subject) for entry in self.tasks]
        return tupleList

    def insert_task(self, task_num, assignment, status, duedate, subject):
        newEntry = TaskEntry(task_num=task_num, assignment=assignment, status=status, duedate=duedate, subject=subject)
        self.tasks.append(newEntry)

    def remove_task(self, task_num):
        for entry in self.tasks:
            if entry.task_num == task_num:
                self.tasks.remove(entry)

    def update_task(self, new_assignment, new_status, new_duedate, new_subject, task_num):
        for entry in self.tasks:
            if entry.task_num == task_num:
                setattr(entry, "assignment", new_assignment)
                setattr(entry, "status", new_status)
                setattr(entry, "duedate", new_duedate)
                setattr(entry, "subject", new_subject)

    def export_csv(self):  
        with open(self.dbName, 'w') as f:
            for entry in self.tasks:
                f.write(f"{entry.task_num},{entry.assignment},{entry.status},{entry.duedate},{entry.subject}\n")
            
    def task_exists(self, task_num):
        for val in self.tasks:
            if val.task_num == task_num:
                return True
            else:
                return False
            
    def import_csv(self):
        options = ["In Progress", "Done", "To Start", "Planning"]
        csvfile = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Choose a csv file to import into the database.")
        with open(csvfile, "r") as f:
            readfile = f.readlines()
            for line in readfile:
                info = line.strip().split(",")
                if info[2] not in options:
                    continue
                else:
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

