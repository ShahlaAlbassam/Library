import tkinter as tk
from tkinter import messagebox, ttk
from database import get_connection


def add_member_gui():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()

    if not name or not email or not phone:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO member (Member_name, email, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Member added successfully!")
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        load_members()


def load_members():
    for item in tree.get_children():
        tree.delete(item)

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM member"
        cursor.execute(query)
        members = cursor.fetchall()
        for member in members:
            tree.insert("", tk.END, values=member)
        cursor.close()
        conn.close()


root = tk.Tk()
root.title("Members Management")
root.geometry("600x500")
root.configure(bg="#F5F5DC")

frame_input = tk.LabelFrame(root, text=" Add New Member ", bg="#F5F5DC", font=("Arial", 11, "bold"))
frame_input.pack(fill="x", padx=15, pady=10)

tk.Label(frame_input, text="Name:", bg="#F5F5DC").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_input, width=35)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Email:", bg="#F5F5DC").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_email = tk.Entry(frame_input, width=35)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Phone:", bg="#F5F5DC").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_phone = tk.Entry(frame_input, width=35)
entry_phone.grid(row=2, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_input, text="Add Member", bg="#8B4513", fg="white", font=("Arial", 10, "bold"),
                    command=add_member_gui)
btn_add.grid(row=3, columnspan=2, pady=10)

frame_table = tk.Frame(root, bg="#F5F5DC")
frame_table.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("ID", "Name", "Email", "Phone")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.pack(fill="both", expand=True)

load_members()

root.mainloop()
