import json
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class ToDoList:
    TODO_FILE = "todo_list.json"

    CHOICES = {
        1: 'add_task',
        2: 'mark_complete',
        3: 'view_todo'
    }

    def __init__(self, root):
        self.root = root
        self.root.title("ToDo List App")
        self.load_todo_list()
        #should increase the size of the pop up window to make it more visible
        self.root.geometry("300x300")

        self.style = ttk.Style()
        # self.style.theme_use("plastik")  # Use the 'plastik' theme for a modern look
        self.style.theme_use("clam")

        self.menu_label = ttk.Label(root, text="\nWelcome to ToDo list", font=('Helvetica', 14, 'bold'))
        self.menu_label.pack(pady=2)

        self.choice_var = tk.StringVar()
        self.choice_var.set("1")

        self.menu_options = [("Add a task", "1"), ("Mark a task as completed", "2"), ("View Todo list", "3")]
        for option, value in self.menu_options:
            ttk.Radiobutton(root, text=option, variable=self.choice_var, value=value, style='TRadiobutton').pack(pady=5)

        self.exit_button = ttk.Button(root, text="Exit", command=self.on_exit)
        self.exit_button.pack(pady=15)

        self.perform_button = ttk.Button(root, text="Perform", command=self.perform_operation, style='TButton')
        self.perform_button.pack(pady=15)

    def load_todo_list(self):
        try:
            with open(self.TODO_FILE, 'r') as file:
                self.todo_list = json.load(file)
        except FileNotFoundError:
            self.todo_list = []
        except json.JSONDecodeError:
            self.todo_list = []

    def save_todo_list(self):
        with open(self.TODO_FILE, 'w') as file:
            json.dump(self.todo_list, file)

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a task to add:")
        if task:
            self.todo_list.append({"task": task, "completed": False})
            messagebox.showinfo("Task Added", f"Added task: {task}")

    def mark_complete(self):
        incomplete_tasks = [item["task"] for item in self.todo_list if not item["completed"]]

        if not incomplete_tasks:
            messagebox.showinfo("No Incomplete Tasks", "No incomplete tasks to mark as done.")
            return

        mark_window = tk.Toplevel(self.root)
        mark_window.title("Mark Task as Completed")

        listbox = tk.Listbox(mark_window, selectmode=tk.SINGLE, font=('Helvetica', 12))
        for task in incomplete_tasks:
            listbox.insert(tk.END, task)
        listbox.pack(pady=10)

        def mark_selected_task():
            selected_index = listbox.curselection()
            if selected_index:
                selected_task = incomplete_tasks[selected_index[0]]
                index = [item["task"] for item in self.todo_list].index(selected_task)
                self.todo_list[index]["completed"] = True
                messagebox.showinfo("Task Marked as Done", f"Marked task as done: {selected_task}")
                mark_window.destroy()
            else:
                messagebox.showwarning("No Task Selected", "Please select a task to mark as done.")

        mark_button = ttk.Button(mark_window, text="Mark Selected Task", command=mark_selected_task, style='TButton')
        mark_button.pack()

    def view_todo(self):
        if not self.todo_list:
            messagebox.showinfo("Empty Todo List", "Todo task list is empty.")
            return

        todo_text = "\nTodo list:\n"
        for idx, item in enumerate(self.todo_list, start=1):
            status = "Completed" if item["completed"] else "Incomplete"
            todo_text += f"{idx}) {item['task']} - {status}\n"

        messagebox.showinfo("Todo List", todo_text)

    def on_exit(self):
        self.save_todo_list()
        self.root.destroy()

    def perform_operation(self):
        choice = int(self.choice_var.get())

        if choice == 4:
            self.on_exit()
        elif 1 <= choice <= 3:
            getattr(self, self.CHOICES[choice])()
        else:
            messagebox.showwarning("Invalid Input", "Please provide a valid input.")

if __name__ == "__main__":
    root = tk.Tk()
    todo_list_app = ToDoList(root)
    root.mainloop()