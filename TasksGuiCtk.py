import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from TasksSqlite import TaskSqlite
from tkinter import filedialog as fd

class TaskGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=TaskSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Task Manager')
        self.geometry('1800x2880')
        self.config(bg='#F5F5DC')
        self.resizable(False, False)

        self.font1 = ('Montserrat', 30, 'bold')
        self.font2 = ('Montserrat', 12, 'bold')

        # Data Entry Form
        # 'Task Number' Label and Entry Widgets
        self.num_label = self.newCtkLabel(text='Task Num:')
        self.num_label.place(x=40, y=40)
        self.num_entry = self.newCtkEntry()
        self.num_entry.place(x=220, y=40)

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Task:')
        self.name_label.place(x=40, y=200)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=220, y=200)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status:')
        self.status_label.place(x=40, y=360)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Done', 'Started', 'Planning', 'None']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=220, y=360)

        # 'Due Date' Label and Combo Box Widgets
        self.due_label = self.newCtkLabel('Due Date:')
        self.due_label.place(x=40, y=520)
        self.due_entry = self.newCtkEntry()
        self.due_entry.place(x=220, y=520)


        # 'subject' Label and Combo Box Widgets
        self.subject_label = self.newCtkLabel('Subject:')
        self.subject_label.place(x=40, y=680)
        self.subject_entry = self.newCtkEntry()
        self.subject_entry.place(x=220, y=680)


        self.importcsv_button = self.newCtkButton(text="Import Data",
                                onClickHandler=self.import_to_csv,
                                fgColor='#363031',
                                hoverColor='#363031',
                                borderColor='#363031')
        self.importcsv_button.place(x=787, y=850)

        self.exportjson_button = self.newCtkButton(text="Export JSON", onClickHandler=self.export_to_json, 
                                fgColor='#363031',
                                hoverColor='#363031',
                                borderColor='#363031')
        self.exportjson_button.place(x=1387, y=850)

        self.add_button = self.newCtkButton(text='Add Task',
                                onClickHandler=self.add_entry,
                                fgColor='#363031',
                                hoverColor='#363031',
                                borderColor='#363031')
        self.add_button.place(x=187,y=850)

        self.new_button = self.newCtkButton(text='New Task',
                                onClickHandler=lambda:self.clear_form(True), fgColor='#363031',
                                hoverColor='#363031',
                                borderColor='#363031')
        self.new_button.place(x=80,y=1100)

        self.update_button = self.newCtkButton(text='Update Task',
                                    onClickHandler=self.update_entry, fgColor='#363031',
                                hoverColor='#363031',
                                borderColor='#363031')
        self.update_button.place(x=580,y=1100)

        self.delete_button = self.newCtkButton(text='Delete Task',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#363031',
                                hoverColor='#363031',
                                borderColor='#363031')
        self.delete_button.place(x=1080,y=1100)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv, fgColor='#363031',
                                hoverColor='#363031',
                                borderColor='#363031')
        self.export_button.place(x=1580,y=1100)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#000000',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=25)
        self.tree['columns'] = ('Task Number', 'Assignment', 'Status', 'Due Date', 'Subject')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Task Number', anchor=tk.CENTER, width=10)
        self.tree.column('Assignment', anchor=tk.CENTER, width=150)
        self.tree.column('Status', anchor=tk.CENTER, width=150)
        self.tree.column('Due Date', anchor=tk.CENTER, width=40)
        self.tree.column('Subject', anchor=tk.CENTER, width=150)

        self.tree.heading('Task Number', text='Task Number')
        self.tree.heading('Assignment', text='Assignment')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.heading('Subject', text='Subject')

        self.tree.place(x=600, y=20, width=1700, height=750)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.tree.tag_configure("Started", background="#0000FF")
        self.tree.tag_configure("Done", background="green")
        self.tree.tag_configure("None", background="#FF0000")
        self.tree.tag_configure("Planning", background="yellow")

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000000'
        widget_BgColor='#F5F5DC'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#000000'
        widget_BorderWidth=4
        widget_Width=350

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=350
        widget_height = 35
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly', height=widget_height)
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#F5F5DC', bgColor='#F5F5DC', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=350
        widget_height = 35
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width, height=widget_height)
       
        return widget

    # Handles
    def add_to_treeview(self):
        tasks = self.db.tasklist()
        self.tree.delete(*self.tree.get_children())
        tag = "normal"
        for task in tasks:
            if task[2] == "Started":
                tag = "Started"
            elif task[2] == "Planning":
                tag = "Planning"
            elif task[2] == "None":
                tag = "None"
            elif task[2] == "Done":
                tag = "Done"
            print(task)
            self.tree.insert('', END, values=task, tags=(tag))

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.num_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.status_cboxVar.set('To Start')
        self.due_entry.delete(0, END)
        self.subject_entry.delete(0, END)

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.num_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.status_cboxVar.set(row[2])
            self.due_entry.insert(0, row[3])
            self.subject_entry.insert(0, row[4])
        else:
            pass

    def add_entry(self):
        id=self.num_entry.get()
        name=self.name_entry.get()
        status=self.status_cboxVar.get()
        due=self.due_entry.get()
        sub=self.subject_entry.get()

        if not (id and name and status and due and sub):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.task_exists(id):
            messagebox.showerror('Error', 'Task already exists')
        else:
            self.db.insert_task(id, name, status, due, sub)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a task to delete')
        else:
            tasknum = self.num_entry.get()
            self.db.remove_task(tasknum)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to update')
        else:
            id=self.num_entry.get()
            name=self.name_entry.get()
            status=self.status_cboxVar.get()
            due=self.due_entry.get()
            sub=self.subject_entry.get()
            self.db.update_task(name, status, due, sub, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}')

    def import_to_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo("Success", "Data has been imported into the database.")

    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success', f'Data exported to {self.db.json}')



