import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from database import get_connection

class BooksUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - Books")
        self.root.geometry("1000x650")
        self.root.configure(bg="#F2F4F7")
        self.root.configure(bg="#D2B48C")
        button_color = "#8B5E3C"
        button_text_color = "white"

        self.selected_id = None

        # Main Title
        tk.Label(
            root,
            text="Book Management",
            font=("Arial", 22, "bold"),
            bg="#F2F4F7",
            fg="#243B53"
        ).pack(pady=15)

        # Book Information Frame
        input_frame = tk.LabelFrame(
            root,
            text="Book Information",
            font=("Arial", 12, "bold"),
            bg="#F2F4F7",
            padx=15,
            pady=10
        )
        input_frame.pack(fill="x", padx=20, pady=10)

        # Book ID
        tk.Label(
            input_frame,
            text="Book ID:",
            bg="#F2F4F7"
        ).grid(row=0, column=0, padx=5, pady=8)

        self.id_entry = tk.Entry(input_frame, width=25)
        self.id_entry.grid(row=0, column=1, padx=5, pady=8)

        # Title
        tk.Label(
            input_frame,
            text="Title:",
            bg="#F2F4F7"
        ).grid(row=0, column=2, padx=5, pady=8)

        self.title_entry = tk.Entry(input_frame, width=25)
        self.title_entry.grid(row=0, column=3, padx=5, pady=8)

        # Author
        tk.Label(
            input_frame,
            text="Author:",
            bg="#F2F4F7"
        ).grid(row=1, column=0, padx=5, pady=8)

        self.author_entry = tk.Entry(input_frame, width=25)
        self.author_entry.grid(row=1, column=1, padx=5, pady=8)

        # Category
        tk.Label(
            input_frame,
            text="Category:",
            bg="#F2F4F7"
        ).grid(row=1, column=2, padx=5, pady=8)

        self.category_entry = tk.Entry(input_frame, width=25)
        self.category_entry.grid(row=1, column=3, padx=5, pady=8)

        # Status
        tk.Label(
            input_frame,
            text="Status:",
            bg="#F2F4F7"
        ).grid(row=2, column=0, padx=5, pady=8)

        self.status_combo = ttk.Combobox(
            input_frame,
            values=["Available", "Borrowed"],
            state="readonly",
            width=22
        )
        self.status_combo.grid(row=2, column=1, padx=5, pady=8)
        self.status_combo.set("Available")

        # Buttons Frame
        button_frame = tk.Frame(root, bg="#F2F4F7")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Book",
            width=13,
            command=self.add_book,
            bg=button_color,
            fg=button_text_color,
            activebackground="#5D4037",
            activeforeground="white"
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update Book",
            width=13,
            command=self.update_book,
            bg=button_color,
            fg=button_text_color,
            activebackground="#5D4037",
            activeforeground="white"
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete Book",
            width=13,
            command=self.delete_book,
            bg=button_color,
            fg=button_text_color,
            activebackground="#5D4037",
            activeforeground="white"
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Clear Fields",
            width=13,
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)

        # Search Frame
        search_frame = tk.Frame(root, bg="#F2F4F7")
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            search_frame,
            text="Search Book:",
            bg="#F2F4F7",
            font=("Arial", 11)
        ).pack(side="left", padx=5)

        self.search_entry = tk.Entry(search_frame, width=35)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_book
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_books
        ).pack(side="left", padx=5)

        # Books Table
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "Book ID",
            "Title",
            "Author",
            "Category",
            "Status"
        )

        self.book_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.book_table.heading(column, text=column)

        self.book_table.column("Book ID", width=80, anchor="center")
        self.book_table.column("Title", width=200)
        self.book_table.column("Author", width=180)
        self.book_table.column("Category", width=150)
        self.book_table.column("Status", width=150)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.book_table.yview
        )

        self.book_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.book_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        self.book_table.bind(
            "<<TreeviewSelect>>",
            self.select_book
        )

        # Load books
        self.load_books()

        # READ: Display all books

    def load_books(self):
        conn = None
        cursor = None

        try:
            conn = get_connection()

            if conn is None:
                messagebox.showerror(
                    "Database Error",
                    "Could not connect to database."
                )
                return

            cursor = conn.cursor()

            cursor.execute(
                "SELECT book_id, title, author, category, status FROM books"
            )

            records = cursor.fetchall()

            self.book_table.delete(
                *self.book_table.get_children()
            )

            for row in records:
                self.book_table.insert(
                    "",
                    "end",
                    values=row
                )

        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

# CREATE: Add a new book
    def add_book(self):
        book_id = self.id_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        status = self.status_combo.get()

        if not book_id or not title or not author:
            messagebox.showwarning(
                "Missing Information",
                "Please enter Book ID, Title and Author."
            )
            return

        try:
            book_id = int(book_id)
        except ValueError:
            messagebox.showwarning(
                "Invalid ID",
                "Book ID must be a number."
            )
            return

        conn = None
        cursor = None

        try:
            conn = get_connection()

            if conn is None:
                messagebox.showerror(
                    "Database Error",
                    "Could not connect to database."
                )
                return

            cursor = conn.cursor()

            sql = """
                INSERT INTO books
                (book_id, title, author, category, status)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                book_id,
                title,
                author,
                category,
                status
            )

            cursor.execute(sql, values)
            conn.commit()

            messagebox.showinfo(
                "Success",
                "Book added successfully!"
            )

            self.clear_fields()
            self.load_books()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # SEARCH: Search for books
    def search_book(self):
        keyword = self.search_entry.get().strip()

        conn = None
        cursor = None

        try:
            conn = get_connection()

            if conn is None:
                messagebox.showerror(
                    "Database Error",
                    "Could not connect to database."
                )
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

            search_value = "%" + keyword + "%"

            cursor.execute(
                sql,
                (
                    search_value,
                    search_value,
                    search_value,
                    search_value
                )
            )

            records = cursor.fetchall()

            self.book_table.delete(
                *self.book_table.get_children()
            )

            for row in records:
                self.book_table.insert(
                    "",
                    "end",
                    values=row
                )

            if not records:
                messagebox.showinfo(
                    "Search",
                    "No books found."
                )

        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
# Select a book from the table
    def select_book(self, event):
        selected = self.book_table.selection()

        if selected:
            values = self.book_table.item(
                selected[0],
                "values"
            )

            self.selected_id = values[0]

            self.id_entry.config(state="normal")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.id_entry.config(state="disabled")

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[1])

            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, values[2])

            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, values[3])

            self.status_combo.set(values[4])

    # UPDATE: Modify book information
    def update_book(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a book from the table first."
            )
            return

        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        status = self.status_combo.get()

        if not title or not author:
            messagebox.showwarning(
                "Missing Information",
                "Please enter Title and Author."
            )
            return

        conn = None
        cursor = None

        try:
            conn = get_connection()

            if conn is None:
                messagebox.showerror(
                    "Database Error",
                    "Could not connect to database."
                )
                return

            cursor = conn.cursor()

            sql = """
                UPDATE books
                SET title = %s,
                    author = %s,
                    category = %s,
                    status = %s
                WHERE book_id = %s
            """

            values = (
                title,
                author,
                category,
                status,
                self.selected_id
            )

            cursor.execute(sql, values)
            conn.commit()

            messagebox.showinfo(
                "Success",
                "Book updated successfully!"
            )

            self.clear_fields()
            self.load_books()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # DELETE: Remove a book
    def delete_book(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a book from the table first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this book?"
        )

        if confirm:
            conn = None
            cursor = None

            try:
                conn = get_connection()

                if conn is None:
                    messagebox.showerror(
                        "Database Error",
                        "Could not connect to database."
                    )
                    return

                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM books WHERE book_id = %s",
                    (self.selected_id,)
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Book deleted successfully!"
                )

                self.clear_fields()
                self.load_books()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))

            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

    # Clear all fields

    def clear_fields(self):
        self.selected_id = None

        self.id_entry.config(state="normal")
        self.id_entry.delete(0, tk.END)

        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

        self.status_combo.set("Available")
        self.search_entry.delete(0, tk.END)

        self.book_table.selection_remove(
            self.book_table.selection()
        )

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BooksUI(root)
    root.mainloop()

