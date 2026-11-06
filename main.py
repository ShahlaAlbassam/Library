import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
from database import get_connection

root = tk.Tk()
root.title("BookHaven - Library Management System")
root.geometry("1100x750")

bg_color = "#F5EBE0"
card_bg = "#EEDDC3"
btn_color = "#5C4033"
text_color = "#3E2723"
sub_text = "#7A6858"

root.configure(bg=bg_color)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", foreground=text_color, rowheight=25, fieldbackground="white")
style.configure("Treeview.Heading", background=btn_color, foreground="white", font=("Arial", 10, "bold"))
style.configure("Custom.TButton", background=btn_color, foreground="white", font=("Arial", 9, "bold"))
style.configure("Danger.TButton", background="#A93226", foreground="white", font=("Arial", 9, "bold"))
style.configure("Gray.TButton", background="#D5D8DC", foreground=text_color, font=("Arial", 9, "bold"))

style.configure("TNotebook", background=bg_color, borderwidth=0)
style.configure("TNotebook.Tab", background="#D2B48C", foreground="black", font=("Arial", 10, "bold"), padding=[15, 5])
style.map("TNotebook.Tab", background=[("selected", btn_color)], foreground=[("selected", "white")])

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ==========================================
# TAB 1: MEMBERS MANAGEMENT
# ==========================================
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

frame_m_input = tk.LabelFrame(tab_members, text=" Add New Member ", bg=bg_color, fg=text_color, font=("Arial", 11, "bold"))
frame_m_input.pack(fill="x", padx=15, pady=10)

tk.Label(frame_m_input, text="Name:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=0, column=0, padx=8, pady=8, sticky="w")
entry_m_name = tk.Entry(frame_m_input, width=35, bg="white", fg=text_color, relief="solid", bd=1)
entry_m_name.grid(row=0, column=1, padx=8, pady=8)

tk.Label(frame_m_input, text="Email:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=1, column=0, padx=8, pady=8, sticky="w")
entry_m_email = tk.Entry(frame_m_input, width=35, bg="white", fg=text_color, relief="solid", bd=1)
entry_m_email.grid(row=1, column=1, padx=8, pady=8)

tk.Label(frame_m_input, text="Phone:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=2, column=0, padx=8, pady=8, sticky="w")
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

scrollbar_m = ttk.Scrollbar(frame_m_table, orient="vertical", command=tree_members.yview)
tree_members.configure(yscrollcommand=scrollbar_m.set)

tree_members.pack(side="left", fill="both", expand=True)
scrollbar_m.pack(side="right", fill="y")


# ==========================================
# TAB 2: BOOKS MANAGEMENT
# ==========================================
tab_books = tk.Frame(notebook, bg=bg_color)
notebook.add(tab_books, text=" Books Management ")

selected_book_id = None

def load_books():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT book_id, title, author, category, status FROM books")
        records = cursor.fetchall()

        book_table.delete(*book_table.get_children())
        for row in records:
            book_table.insert("", "end", values=row)

        for widget in cards_frame.winfo_children():
            widget.destroy()

        for i, row in enumerate(records[:3]):
            book_id, title, author, category, status = row

            card = tk.Frame(cards_frame, bg=card_bg, width=320, height=105, relief="solid", bd=1)
            card.grid(row=0, column=i, padx=5, pady=2)
            card.pack_propagate(False)

            cover_box = tk.Frame(card, bg=btn_color, width=65, height=85)
            cover_box.place(x=10, y=10)
            cover_box.pack_propagate(False)

            short_title = title if len(title) <= 18 else title[:16] + "..."
            tk.Label(
                cover_box,
                text=short_title,
                fg="white",
                bg=btn_color,
                font=("Arial", 8, "bold"),
                wraplength=55,
                justify="center"
            ).pack(expand=True, padx=2, pady=2)

            tk.Label(card, text=category.upper() if category else "GENERAL", font=("Arial", 8, "bold"), bg=card_bg, fg=sub_text).place(x=85, y=12)

            title_text = title if len(title) < 20 else title[:18] + "..."
            tk.Label(card, text=title_text, font=("Arial", 10, "bold"), bg=card_bg, fg=text_color).place(x=85, y=32)

            author_text = f"By {author}" if len(author) < 20 else f"By {author[:15]}..."
            tk.Label(card, text=author_text, font=("Arial", 9), bg=card_bg, fg=sub_text).place(x=85, y=55)

            status_text = f"Status: {status}"
            tk.Label(card, text=status_text, font=("Arial", 8), bg=card_bg, fg="#A93226" if status == "Borrowed" else "#196F3D").place(x=85, y=80)

    except mysql.connector.Error as e:
        print("Error loading books:", e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

def add_book():
    book_id = id_entry.get().strip()
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    category = category_entry.get().strip()
    status = status_combo.get()

    if not book_id or not title or not author:
        messagebox.showwarning("Missing Information", "Please enter Book ID, Title and Author.")
        return

    try:
        book_id = int(book_id)
    except ValueError:
        messagebox.showwarning("Invalid ID", "Book ID must be a number.")
        return

    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        sql = "INSERT INTO books (book_id, title, author, category, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (book_id, title, author, category, status))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        clear_book_fields()
        load_books()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

def search_book():
    keyword = search_entry.get().strip()
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        sql = """
              SELECT book_id, title, author, category, status
              FROM books
              WHERE CAST(book_id AS CHAR) LIKE %s
                 OR title LIKE %s
                 OR author LIKE %s
                 OR category LIKE %s
              """
        val = "%" + keyword + "%"
        cursor.execute(sql, (val, val, val, val))
        records = cursor.fetchall()
        book_table.delete(*book_table.get_children())
        for row in records:
            book_table.insert("", "end", values=row)
        if not records:
            messagebox.showinfo("Search", "No books found.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

def select_book(event):
    global selected_book_id
    selected = book_table.selection()
    if selected:
        values = book_table.item(selected[0], "values")
        selected_book_id = values[0]
        id_entry.config(state="normal", bg="white")
        id_entry.delete(0, tk.END)
        id_entry.insert(0, values[0])
        id_entry.config(state="readonly", bg="#EBEBE4")

        title_entry.delete(0, tk.END)
        title_entry.insert(0, values[1])

        author_entry.delete(0, tk.END)
        author_entry.insert(0, values[2])

        category_entry.delete(0, tk.END)
        category_entry.insert(0, values[3])

        status_combo.set(values[4])

def update_book():
    global selected_book_id
    if selected_book_id is None:
        messagebox.showwarning("No Selection", "Please select a book from the table first.")
        return
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    category = category_entry.get().strip()
    status = status_combo.get()

    if not title or not author:
        messagebox.showwarning("Missing Information", "Please enter Title and Author.")
        return

    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        sql = "UPDATE books SET title = %s, author = %s, category = %s, status = %s WHERE book_id = %s"
        cursor.execute(sql, (title, author, category, status, selected_book_id))
        conn.commit()
        messagebox.showinfo("Success", "Book updated successfully!")
        clear_book_fields()
        load_books()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

def delete_book():
    global selected_book_id
    if selected_book_id is None:
        messagebox.showwarning("No Selection", "Please select a book from the table first.")
        return
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn is None:
                return
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id = %s", (selected_book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book deleted successfully!")
            clear_book_fields()
            load_books()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

def clear_book_fields():
    global selected_book_id
    selected_book_id = None
    id_entry.config(state="normal", bg="white")
    id_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    status_combo.set("Available")
    search_entry.delete(0, tk.END)
    if book_table.selection():
        book_table.selection_remove(book_table.selection())

input_frame_b = tk.LabelFrame(tab_books, text="BOOK DETAILS", font=("Arial", 11, "bold"), bg=bg_color, fg=text_color, padx=15, pady=10)
input_frame_b.pack(fill="x", padx=15, pady=5)

tk.Label(input_frame_b, text="Book ID:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=6, sticky="w")
id_entry = tk.Entry(input_frame_b, width=22, bg="white", fg=text_color, relief="solid", bd=1)
id_entry.grid(row=0, column=1, padx=5, pady=6)

tk.Label(input_frame_b, text="Title *:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=6, sticky="w")
title_entry = tk.Entry(input_frame_b, width=22, bg="white", fg=text_color, relief="solid", bd=1)
title_entry.grid(row=0, column=3, padx=5, pady=6)

tk.Label(input_frame_b, text="Author *:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=6, sticky="w")
author_entry = tk.Entry(input_frame_b, width=22, bg="white", fg=text_color, relief="solid", bd=1)
author_entry.grid(row=1, column=1, padx=5, pady=6)

tk.Label(input_frame_b, text="Category:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=6, sticky="w")
category_entry = tk.Entry(input_frame_b, width=22, bg="white", fg=text_color, relief="solid", bd=1)
category_entry.grid(row=1, column=3, padx=5, pady=6)

tk.Label(input_frame_b, text="Status:", bg=bg_color, fg=text_color, font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=6, sticky="w")
status_combo = ttk.Combobox(input_frame_b, values=["Available", "Borrowed"], state="readonly", width=20)
status_combo.grid(row=2, column=1, padx=5, pady=6)
status_combo.set("Available")

button_frame_b = tk.Frame(tab_books, bg=bg_color)
button_frame_b.pack(pady=5)

ttk.Button(button_frame_b, text="+ Add Book", command=add_book, style="Custom.TButton").grid(row=0, column=0, padx=5, ipadx=5, ipady=3)
ttk.Button(button_frame_b, text="Update Book", command=update_book, style="Custom.TButton").grid(row=0, column=1, padx=5, ipadx=5, ipady=3)
ttk.Button(button_frame_b, text="Delete Book", command=delete_book, style="Danger.TButton").grid(row=0, column=2, padx=5, ipadx=5, ipady=3)
ttk.Button(button_frame_b, text="Clear Form", command=clear_book_fields, style="Gray.TButton").grid(row=0, column=3, padx=5, ipadx=5, ipady=3)

cards_frame = tk.Frame(tab_books, bg=bg_color)
cards_frame.pack(fill="x", padx=15, pady=2)

search_frame_b = tk.Frame(tab_books, bg=bg_color)
search_frame_b.pack(fill="x", padx=15, pady=2)

tk.Label(search_frame_b, text="Search Book:", bg=bg_color, fg=text_color, font=("Arial", 10, "bold")).pack(side="left", padx=5)
search_entry = tk.Entry(search_frame_b, width=25, bg="white", fg=text_color, relief="solid", bd=1)
search_entry.pack(side="left", padx=5)

ttk.Button(search_frame_b, text="Search", command=search_book, style="Custom.TButton").pack(side="left", padx=3)
ttk.Button(search_frame_b, text="Show All", command=load_books, style="Gray.TButton").pack(side="left", padx=3)

table_frame_b = tk.Frame(tab_books, bg=bg_color)
table_frame_b.pack(fill="both", expand=True, padx=15, pady=5)

columns_b = ("Book ID", "Title", "Author", "Category", "Status")
book_table = ttk.Treeview(table_frame_b, columns=columns_b, show="headings")
for col in columns_b:
    book_table.heading(col, text=col)

book_table.column("Book ID", width=70, anchor="center")
book_table.column("Title", width=200)
book_table.column("Author", width=160)
book_table.column("Category", width=130)
book_table.column("Status", width=100, anchor="center")

scrollbar_b = ttk.Scrollbar(table_frame_b, orient="vertical", command=book_table.yview)
book_table.configure(yscrollcommand=scrollbar_b.set)
book_table.pack(side="left", fill="both", expand=True)
scrollbar_b.pack(side="right", fill="y")
book_table.bind("<<TreeviewSelect>>", select_book)


# ==========================================
# TAB 3: BORROWINGS MANAGEMENT
# ==========================================
tab_borrow = tk.Frame(notebook, bg=bg_color)
notebook.add(tab_borrow, text=" Borrowings Management ")

def fetch_members_list():
    conn = get_connection()
    members = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Member_name FROM Member")
            result = cursor.fetchall()
            members = [row[0] for row in result]
            conn.close()
        except Exception as e:
            print(f"Error fetching members: {e}")
    return members if members else ["No Members in DB"]

def fetch_books_list():
    conn = get_connection()
    books = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM books")
            result = cursor.fetchall()
            books = [row[0] for row in result]
            conn.close()
        except Exception as e:
            print(f"Error fetching books: {e}")
    return books if books else ["No Books in DB"]

def load_active_borrowings():
    for widget in records_scroll.winfo_children():
        widget.destroy()

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Borrow_ID, member_name, book_title, borrow_date, due_date, status FROM borrow")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                row_text = f"REF: {row[0]}  |  {row[1]}  |  {row[2]}  |  Issued: {row[3]}  |  Due: {row[4]}  |  [{row[5]}]"
                lbl = tk.Label(
                    records_scroll,
                    text=row_text,
                    font=("Arial", 10),
                    bg="white",
                    fg=text_color,
                    anchor="w"
                )
                lbl.pack(fill="x", padx=5, pady=4)
        except Exception as e:
            print(f"Error loading records: {e}")

def issue_book_action():
    selected_member = member_dropdown.get()
    selected_book = book_dropdown.get()
    issue_date = issue_date_entry.get()
    due_date = due_date_entry.get()

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO borrow (member_name, book_title, borrow_date, due_date, status) VALUES (%s, %s, %s, %s, %s)"
            values = (selected_member, selected_book, issue_date, due_date, "Active")
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book issued successfully!")
            load_active_borrowings()
            load_books()
        except Exception as e:
            messagebox.showerror("Error", f"Error issuing book: {e}")

form_frame_br = tk.LabelFrame(tab_borrow, text=" ISSUE A BOOK ", font=("Arial", 11, "bold"), bg=bg_color, fg=text_color, padx=15, pady=10)
form_frame_br.place(x=30, y=20, width=420, height=450)

tk.Label(form_frame_br, text="Select member *", bg=bg_color, fg=text_color, font=("Arial", 10)).place(x=20, y=20)
members_list_val = fetch_members_list()
member_dropdown = ttk.Combobox(form_frame_br, values=members_list_val, state="readonly", width=35)
if members_list_val:
    member_dropdown.set(members_list_val[0])
member_dropdown.place(x=20, y=45)

tk.Label(form_frame_br, text="Select book *", bg=bg_color, fg=text_color, font=("Arial", 10)).place(x=20, y=90)
books_list_val = fetch_books_list()
book_dropdown = ttk.Combobox(form_frame_br, values=books_list_val, state="readonly", width=35)
if books_list_val:
    book_dropdown.set(books_list_val[0])
book_dropdown.place(x=20, y=115)

tk.Label(form_frame_br, text="Issue date", bg=bg_color, fg=text_color, font=("Arial", 10)).place(x=20, y=160)
issue_date_entry = tk.Entry(form_frame_br, width=18, bg="white", fg=text_color, relief="solid", bd=1)
issue_date_entry.place(x=20, y=185)
issue_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Label(form_frame_br, text="Due date", bg=bg_color, fg=text_color, font=("Arial", 10)).place(x=210, y=160)
due_date_entry = tk.Entry(form_frame_br, width=18, bg="white", fg=text_color, relief="solid", bd=1)
due_date_entry.place(x=210, y=185)
due_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

issue_button = ttk.Button(form_frame_br, text="Issue Book ->", command=issue_book_action, style="Custom.TButton")
issue_button.place(x=20, y=250, width=340, height=35)

table_frame_br = tk.LabelFrame(tab_borrow, text=" ACTIVE BORROWINGS ", font=("Arial", 11, "bold"), bg=bg_color, fg=text_color, padx=10, pady=10)
table_frame_br.place(x=470, y=20, width=580, height=450)

header_frame = tk.Frame(table_frame_br, bg="#F9F5F0", height=35, relief="solid", bd=1)
header_frame.pack(fill="x", padx=10, pady=5)
header_frame.pack_propagate(False)

tk.Label(header_frame, text="Active records listed below from database database records.", font=("Arial", 9, "bold"), bg="#F9F5F0", fg=sub_text).pack(side="left", padx=10, pady=8)

records_scroll = tk.CTkScrollableFrame if 'ctk' in globals() else None # fallback frame if needed
# Using standard tkinter Frame with Canvas/Scrollbar for safety across pure tk environments:
container_canvas_frame = tk.Frame(table_frame_br, bg="white")
container_canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

records_scroll = tk.Frame(container_canvas_frame, bg="white")
records_scroll.pack(fill="both", expand=True)

# Initial data loads
load_members()
load_books()
load_active_borrowings()

root.mainloop()
