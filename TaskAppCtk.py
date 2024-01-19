from Tasks import Tasks
from TasksGuiCtk import TaskGuiCtk

def main():
    db = Tasks(init=False, dbName='Tasks.csv')
    app = TaskGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()