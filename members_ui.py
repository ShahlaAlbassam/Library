import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

root = tk.Tk()
root.title("Members Management")
root.geometry("700x500")
root.configure(bg="#F5F5DC")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

tab_members = tk.Frame(notebook, bg="#F5F5DC")
notebook.add(tab_members, text=" Members ")


def add_member_gui():
    name = entry_m_name.get()
    email = entry_m_email.get()
    phone = entry_m_phone.get()

    if not name or not email or not phone:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO member (Member_name, email, phone) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, phone))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Member added successfully!")
            entry_m_name.delete(0, tk.END)
            entry_m_email.delete(0, tk.END)
            entry_m_phone.delete(0, tk.END)
            load_members()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add member: {e}")


def load_members():
    for item in tree_members.get_children():
        tree_members.delete(item)

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM member"
        cursor.execute(query)
        members = cursor.fetchall()
        for member in members:
            tree_members.insert("", tk.END, values=member)
        cursor.close()
        conn.close()


frame_m_input = tk.LabelFrame(tab_members, text=" Add New Member ", bg="#F5F5DC", font=("Arial", 11, "bold"))
frame_m_input.pack(fill="x", padx=15, pady=10)

tk.Label(frame_m_input, text="Name:", bg="#F5F5DC").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_m_name = tk.Entry(frame_m_input, width=35)
entry_m_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_m_input, text="Email:", bg="#F5F5DC").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_m_email = tk.Entry(frame_m_input, width=35)
entry_m_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_m_input, text="Phone:", bg="#F5F5DC").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_m_phone = tk.Entry(frame_m_input, width=35)
entry_m_phone.grid(row=2, column=1, padx=5, pady=5)

btn_m_add = tk.Button(frame_m_input, text="Add Member", bg="#8B4513", fg="white", font=("Arial", 10, "bold"),
                      command=add_member_gui)
btn_m_add.grid(row=3, column=0, columnspan=2, pady=10)

frame_m_table = tk.Frame(tab_members, bg="#F5F5DC")
frame_m_table.pack(fill="both", expand=True, padx=15, pady=10)

m_columns = ("ID", "Name", "Email", "Phone")
tree_members = ttk.Treeview(frame_m_table, columns=m_columns, show="headings")
for col in m_columns:
    tree_members.heading(col, text=col)
    tree_members.column(col, width=140, anchor="center")
tree_members.pack(fill="both", expand=True)

load_members()

root.mainloop()
