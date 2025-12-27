import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ---------- DATABASE ----------
conn = sqlite3.connect("todo.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    status TEXT,
    created_at TEXT
)
""")
conn.commit()

# ---------- FUNCTIONS ----------
def load_tasks():
    listbox.delete(0, tk.END)
    cur.execute("SELECT * FROM tasks")
    for row in cur.fetchall():
        status = "✔" if row[2] == "Done" else "✗"
        listbox.insert(tk.END, f"{row[0]}. {status} {row[1]} ({row[3]})")

def add_task():
    task = entry.get()
    if task == "":
        messagebox.showwarning("Warning", "Task cannot be empty")
        return

    date_time = datetime.now().strftime("%d-%m-%Y %H:%M")
    cur.execute("INSERT INTO tasks(task,status,created_at) VALUES(?,?,?)",
                (task, "Pending", date_time))
    conn.commit()
    entry.delete(0, tk.END)
    load_tasks()

def mark_done():
    try:
        selected = listbox.get(listbox.curselection())
        task_id = selected.split(".")[0]
        cur.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
        conn.commit()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task first")

def delete_task():
    try:
        selected = listbox.get(listbox.curselection())
        task_id = selected.split(".")[0]
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task first")

# ---------- GUI ----------
root = tk.Tk()
root.title("Advanced To-Do List")
root.geometry("500x550")
root.config(bg="#f8fafc")

tk.Label(root, text="📝 To-Do List App",
         font=("Poppins", 20, "bold"),
         bg="#f8fafc").pack(pady=15)

entry = tk.Entry(root, font=("Poppins", 14))
entry.pack(padx=30, pady=10, fill=tk.X)

btn_frame = tk.Frame(root, bg="#f8fafc")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add",
          bg="#22c55e", fg="white",
          font=("Poppins", 12),
          width=10, command=add_task).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Done",
          bg="#2563eb", fg="white",
          font=("Poppins", 12),
          width=10, command=mark_done).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Delete",
          bg="#ef4444", fg="white",
          font=("Poppins", 12),
          width=10, command=delete_task).grid(row=0, column=2, padx=5)

listbox = tk.Listbox(root,
                     font=("Poppins", 12),
                     height=15,
                     selectbackground="#c7d2fe")
listbox.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)

load_tasks()
root.mainloop()
