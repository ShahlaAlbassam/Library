import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import get_connection


class BorrowingsApp:
    def __init__(self, parent):
        self.parent = parent
        self.bg_color = "#F5EBE0"
        self.card_bg = "#EEDDC3"
        self.btn_color = "#5C4033"
        self.text_color = "#3E2723"
        self.sub_text = "#7A6858"

        main_frame = tk.Frame(self.parent, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

       
        top_bar = tk.Frame(main_frame, bg=self.bg_color)
        top_bar.pack(fill="x", pady=(5, 10))

        tk.Label(
            top_bar,
            text="BORROWINGS MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side="left")

        ttk.Button(
            top_bar,
            text="↻ Refresh",
            command=self.refresh_all,
            style="Gray.TButton"
        ).pack(side="right", ipadx=6, ipady=2)

        # Top Container for Form and Table
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True, padx=0, pady=5)

        # Issue A Book Form Frame (Left Side)
        form_frame = tk.LabelFrame(
            content_frame,
            text="ISSUE A BOOK",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        form_frame.pack(side="left", fill="y", padx=(0, 10), pady=0)

        # Select Member Dropdown
        tk.Label(form_frame, text="Select member *", font=("Arial", 10), bg=self.bg_color, fg=self.text_color).pack(
            anchor="w", pady=(5, 2))
        self.members_mapping = self.fetch_members_dict()
        members_list_val = list(self.members_mapping.keys()) if self.members_mapping else ["No members found"]

        self.member_dropdown = ttk.Combobox(
            form_frame,
            values=members_list_val,
            state="readonly",
            width=32
        )
        self.member_dropdown.pack(pady=(0, 10))
        if members_list_val:
            self.member_dropdown.set(members_list_val[0])

        # Select Book Dropdown
        tk.Label(form_frame, text="Select book *", font=("Arial", 10), bg=self.bg_color, fg=self.text_color).pack(
            anchor="w", pady=(5, 2))
        self.books_mapping = self.fetch_books_dict()
        books_list_val = list(self.books_mapping.keys()) if self.books_mapping else ["No books found"]

        self.book_dropdown = ttk.Combobox(
            form_frame,
            values=books_list_val,
            state="readonly",
            width=32
        )
        self.book_dropdown.pack(pady=(0, 10))
        if books_list_val:
            self.book_dropdown.set(books_list_val[0])

        # Date Entries
        tk.Label(form_frame, text="Issue date", font=("Arial", 10), bg=self.bg_color, fg=self.text_color).pack(
            anchor="w", pady=(5, 2))
        self.issue_date_entry = tk.Entry(form_frame, width=34, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.issue_date_entry.pack(pady=(0, 10))
        self.issue_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(form_frame, text="Due date", font=("Arial", 10), bg=self.bg_color, fg=self.text_color).pack(
            anchor="w", pady=(5, 2))
        self.due_date_entry = tk.Entry(form_frame, width=34, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.due_date_entry.pack(pady=(0, 15))
        self.due_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Issue Button
        ttk.Button(
            form_frame,
            text="Issue Book →",
            command=self.issue_book_action,
            style="Custom.TButton"
        ).pack(fill="x", ipady=3)

        # Active Borrowings Table Frame (Right Side)
        table_container = tk.LabelFrame(
            content_frame,
            text="ACTIVE BORROWINGS",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=10,
            pady=10
        )
        table_container.pack(side="right", fill="both", expand=True, pady=0)

        columns = ("REF", "MEMBER", "BOOK TITLE", "ISSUED", "DUE DATE", "STATUS")
        self.borrow_table = ttk.Treeview(table_container, columns=columns, show="headings", height=15)

        for col in columns:
            self.borrow_table.heading(col, text=col)

        self.borrow_table.column("REF", width=50, anchor="center")
        self.borrow_table.column("MEMBER", width=110)
        self.borrow_table.column("BOOK TITLE", width=140)
        self.borrow_table.column("ISSUED", width=90, anchor="center")
        self.borrow_table.column("DUE DATE", width=90, anchor="center")
        self.borrow_table.column("STATUS", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.borrow_table.yview)
        self.borrow_table.configure(yscrollcommand=scrollbar.set)

        self.borrow_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_active_borrowings()

    def fetch_members_dict(self):
        conn = get_connection()
        members_dict = {}
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Member_id, Member_name FROM member")
                for row in cursor.fetchall():
                    members_dict[f"{row[0]} - {row[1]}"] = row[0]
            except Exception as e:
                print(f"Error fetching members: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn.is_connected():
                    conn.close()
        return members_dict

    def fetch_books_dict(self):
        conn = get_connection()
        books_dict = {}
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT book_id, title FROM books")
                for row in cursor.fetchall():
                    books_dict[f"{row[0]} - {row[1]}"] = row[0]
            except Exception as e:
                print(f"Error fetching books: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn.is_connected():
                    conn.close()
        return books_dict

    def refresh_dropdowns(self):
        current_member = self.member_dropdown.get()
        self.members_mapping = self.fetch_members_dict()
        members_list_val = list(self.members_mapping.keys()) if self.members_mapping else ["No members found"]
        self.member_dropdown["values"] = members_list_val
        if current_member in members_list_val:
            self.member_dropdown.set(current_member)
        elif members_list_val:
            self.member_dropdown.set(members_list_val[0])

        current_book = self.book_dropdown.get()
        self.books_mapping = self.fetch_books_dict()
        books_list_val = list(self.books_mapping.keys()) if self.books_mapping else ["No books found"]
        self.book_dropdown["values"] = books_list_val
        if current_book in books_list_val:
            self.book_dropdown.set(current_book)
        elif books_list_val:
            self.book_dropdown.set(books_list_val[0])

    def refresh_all(self):
        self.refresh_dropdowns()
        self.load_active_borrowings()

    def load_active_borrowings(self):
        for item in self.borrow_table.get_children():
            self.borrow_table.delete(item)

        conn = get_connection()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()
                query = """
                        SELECT b.Borrow_ID, m.Member_name, bk.title, b.borrow_date, b.due_date, b.status
                        FROM borrow b
                        JOIN Member m ON b.Member_id = m.Member_id
                        JOIN books bk ON b.book_id = bk.book_id
                        """
                cursor.execute(query)
                for row in cursor.fetchall():
                    self.borrow_table.insert("", "end", values=row)
            except Exception as e:
                print(f"Error loading records: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn.is_connected():
                    conn.close()

    def issue_book_action(self):
        selected_member_str = self.member_dropdown.get()
        selected_book_str = self.book_dropdown.get()
        issue_date = self.issue_date_entry.get().strip()
        due_date = self.due_date_entry.get().strip()

        if not selected_member_str or not selected_book_str or "No" in selected_member_str:
            messagebox.showwarning("Warning", "Please select a valid member and book.")
            return

        member_id = self.members_mapping.get(selected_member_str)
        book_id = self.books_mapping.get(selected_book_str)

        conn = get_connection()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()
                query = "INSERT INTO borrow (Member_id, book_id, borrow_date, due_date, status) VALUES (%s, %s, %s, %s, %s)"
                values = (member_id, book_id, issue_date, due_date, "Active")
                cursor.execute(query, values)
                conn.commit()
                messagebox.showinfo("Success", "Book issued successfully!")
                self.load_active_borrowings()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                if cursor:
                    cursor.close()
                if conn.is_connected():
                    conn.close()
