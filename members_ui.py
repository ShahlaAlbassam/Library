import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

root = tk.Tk()
root.title("BookHaven - Members Management")
root.geometry("750x550")


bg_color = "#F5EBE0"
btn_color = "#5C4033"
text_color = "#3E2723"

root.configure(bg=bg_color)


style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", foreground=text_color, rowheight=25, fieldbackground="white")
style.configure("Treeview.Heading", background=btn_color, foreground="white", font=("Arial", 10, "bold"))
style.configure("Custom.TButton", background=btn_color, foreground="white", font=("Arial", 9, "bold"))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

tab_members = tk.Frame(notebook, bg=bg_color)
notebook.add(tab_members, text=" Members Management ")


def add_member_gui():
    name = entry_m_name.get().strip()
    email = entry_m_email.get().strip()
    phone = entry_m_phone.get().strip()

    if not name or not email or not phone:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Could not connect to database.")
            return

        cursor = conn.cursor()
        query = "INSERT INTO member (Member_name, email, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        conn.commit()

        messagebox.showinfo("Success", "Member added successfully!")
        entry_m_name.delete(0, tk.END)
        entry_m_email.delete(0, tk.END)
        entry_m_phone.delete(0, tk.END)
        load_members()

    except Exception as e:
        messagebox.showerror("Error", f"Could not add member: {e}")
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()


def load_members():
    for item in tree_members.get_children():
        tree_members.delete(item)

    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM member"
            cursor.execute(query)
            members = cursor.fetchall()
            for member in members:
                tree_members.insert("", tk.END, values=member)
    except Exception as e:
        print("Error loading members:", e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()


frame_m_input = tk.LabelFrame(tab_members, text=" Add New Member ", bg=bg_color, fg=text_color,
                              font=("Arial", 11, "bold"))
frame_m_input.pack(fill="x", padx=15, pady=10)

tk.Label(frame_m_input, text="Name:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=0, column=0, padx=8,
                                                                                           pady=8, sticky="w")
entry_m_name = tk.Entry(frame_m_input, width=35, bg="white", fg=text_color, relief="solid", bd=1)
entry_m_name.grid(row=0, column=1, padx=8, pady=8)

tk.Label(frame_m_input, text="Email:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=1, column=0, padx=8,
                                                                                            pady=8, sticky="w")
entry_m_email = tk.Entry(frame_m_input, width=35, bg="white", fg=text_color, relief="solid", bd=1)
entry_m_email.grid(row=1, column=1, padx=8, pady=8)

tk.Label(frame_m_input, text="Phone:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=2, column=0, padx=8,
                                                                                            pady=8, sticky="w")
entry_m_phone = tk.Entry(frame_m_input, width=35, bg="white", fg=text_color, relief="solid", bd=1)
entry_m_phone.grid(row=2, column=1, padx=8, pady=8)


btn_m_add = ttk.Button(frame_m_input, text="Add Member", command=add_member_gui, style="Custom.TButton")
btn_m_add.grid(row=3, column=0, columnspan=2, pady=12, ipadx=10, ipady=3)

frame_m_table = tk.Frame(tab_members, bg=bg_color)
frame_m_table.pack(fill="both", expand=True, padx=15, pady=10)

m_columns = ("ID", "Name", "Email", "Phone")
tree_members = ttk.Treeview(frame_m_table, columns=m_columns, show="headings")
for col in m_columns:
    tree_members.heading(col, text=col)
    tree_members.column(col, width=150, anchor="center")

scrollbar = ttk.Scrollbar(frame_m_table, orient="vertical", command=tree_members.yview)
tree_members.configure(yscrollcommand=scrollbar.set)

tree_members.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

load_members()

root.mainloop()
