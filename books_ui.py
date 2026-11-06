import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from database import get_connection


class BooksUI:

    def __init__(self, root):
        self.root = root
        self.root.title("BookHaven - Books Management")
        self.root.geometry("1050x680")

        self.bg_color = "#F5EBE0"
        self.btn_color = "#5C4033"
        self.text_color = "#3E2723"

        self.root.configure(bg=self.bg_color)
        self.selected_id = None

        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground=self.text_color, rowheight=25,
                        fieldbackground="white")
        style.configure("Treeview.Heading", background=self.btn_color, foreground="white", font=("Arial", 10, "bold"))

        
        style.configure("Custom.TButton", background=self.btn_color, foreground="white", font=("Arial", 9, "bold"))
        style.configure("Danger.TButton", background="#A93226", foreground="white", font=("Arial", 9, "bold"))
        style.configure("Gray.TButton", background="#D5D8DC", foreground=self.text_color, font=("Arial", 9, "bold"))

        tk.Label(
            root,
            text="BOOKS MANAGEMENT",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=10)

        input_frame = tk.LabelFrame(
            root,
            text="BOOK DETAILS",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=10
        )
        input_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(input_frame, text="Book ID:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=5,
                                                                                                              pady=6,
                                                                                                              sticky="w")
        self.id_entry = tk.Entry(input_frame, width=22, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.id_entry.grid(row=0, column=1, padx=5, pady=6)

        tk.Label(input_frame, text="Title *:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=0,
                                                                                                              column=2,
                                                                                                              padx=5,
                                                                                                              pady=6,
                                                                                                              sticky="w")
        self.title_entry = tk.Entry(input_frame, width=22, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.title_entry.grid(row=0, column=3, padx=5, pady=6)

        tk.Label(input_frame, text="Author *:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=1,
                                                                                                               column=0,
                                                                                                               padx=5,
                                                                                                               pady=6,
                                                                                                               sticky="w")
        self.author_entry = tk.Entry(input_frame, width=22, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.author_entry.grid(row=1, column=1, padx=5, pady=6)

        tk.Label(input_frame, text="Category:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=1,
                                                                                                               column=2,
                                                                                                               padx=5,
                                                                                                               pady=6,
                                                                                                               sticky="w")
        self.category_entry = tk.Entry(input_frame, width=22, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.category_entry.grid(row=1, column=3, padx=5, pady=6)

        tk.Label(input_frame, text="Status:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=2,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=6,
                                                                                                             sticky="w")
        self.status_combo = ttk.Combobox(
            input_frame,
            values=["Available", "Borrowed"],
            state="readonly",
            width=20
        )
        self.status_combo.grid(row=2, column=1, padx=5, pady=6)
        self.status_combo.set("Available")

        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="+ Add Book", command=self.add_book, style="Custom.TButton").grid(row=0, column=0,
                                                                                                        padx=5, ipadx=5,
                                                                                                        ipady=3)
        ttk.Button(button_frame, text="Update Book", command=self.update_book, style="Custom.TButton").grid(row=0,
                                                                                                            column=1,
                                                                                                            padx=5,
                                                                                                            ipadx=5,
                                                                                                            ipady=3)
        ttk.Button(button_frame, text="Delete Book", command=self.delete_book, style="Danger.TButton").grid(row=0,
                                                                                                            column=2,
                                                                                                            padx=5,
                                                                                                            ipadx=5,
                                                                                                            ipady=3)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_fields, style="Gray.TButton").grid(row=0,
                                                                                                          column=3,
                                                                                                          padx=5,
                                                                                                          ipadx=5,
                                                                                                          ipady=3)

        search_frame = tk.Frame(root, bg=self.bg_color)
        search_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(search_frame, text="Search Book:", bg=self.bg_color, fg=self.text_color,
                 font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=30, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.search_entry.pack(side="left", padx=5)

        ttk.Button(search_frame, text="Search", command=self.search_book, style="Custom.TButton").pack(side="left",
                                                                                                       padx=3)
        ttk.Button(search_frame, text="Show All", command=self.load_books, style="Gray.TButton").pack(side="left",
                                                                                                      padx=3)

        table_frame = tk.Frame(root, bg=self.bg_color)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Book ID", "Title", "Author", "Category", "Status")
        self.book_table = ttk.Treeview(table_frame, columns=columns, show="headings")

        for column in columns:
            self.book_table.heading(column, text=column)

        self.book_table.column("Book ID", width=80, anchor="center")
        self.book_table.column("Title", width=220)
        self.book_table.column("Author", width=180)
        self.book_table.column("Category", width=140)
        self.book_table.column("Status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.book_table.yview)
        self.book_table.configure(yscrollcommand=scrollbar.set)

        self.book_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.book_table.bind("<<TreeviewSelect>>", self.select_book)

        self.load_books()

    def load_books(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Could not connect to database.")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, title, author, category, status FROM books")
            records = cursor.fetchall()
            self.book_table.delete(*self.book_table.get_children())
            for row in records:
                self.book_table.insert("", "end", values=row)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def add_book(self):
        book_id = self.id_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        status = self.status_combo.get()

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
                messagebox.showerror("Database Error", "Could not connect to database.")
                return
            cursor = conn.cursor()
            sql = "INSERT INTO books (book_id, title, author, category, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (book_id, title, author, category, status))
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_fields()
            self.load_books()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def search_book(self):
        keyword = self.search_entry.get().strip()
        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Could not connect to database.")
                return
            cursor = conn.cursor()
            sql = """
                  SELECT book_id, title, author, category, status \
                  FROM books
                  WHERE CAST(book_id AS CHAR) LIKE %s \
                     OR title LIKE %s \
                     OR author LIKE %s \
                     OR category LIKE %s \
                  """
            val = "%" + keyword + "%"
            cursor.execute(sql, (val, val, val, val))
            records = cursor.fetchall()
            self.book_table.delete(*self.book_table.get_children())
            for row in records:
                self.book_table.insert("", "end", values=row)
            if not records:
                messagebox.showinfo("Search", "No books found.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def select_book(self, event):
        selected = self.book_table.selection()
        if selected:
            values = self.book_table.item(selected[0], "values")
            self.selected_id = values[0]
            self.id_entry.config(state="normal", bg="white")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.id_entry.config(state="readonly", bg="#EBEBE4")

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[1])

            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, values[2])

            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, values[3])

            self.status_combo.set(values[4])

    def update_book(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Please select a book from the table first.")
            return
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        status = self.status_combo.get()

        if not title or not author:
            messagebox.showwarning("Missing Information", "Please enter Title and Author.")
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Could not connect to database.")
                return
            cursor = conn.cursor()
            sql = "UPDATE books SET title = %s, author = %s, category = %s, status = %s WHERE book_id = %s"
            cursor.execute(sql, (title, author, category, status, self.selected_id))
            conn.commit()
            messagebox.showinfo("Success", "Book updated successfully!")
            self.clear_fields()
            self.load_books()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def delete_book(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Please select a book from the table first.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
            conn = None
            cursor = None
            try:
                conn = get_connection()
                if conn is None:
                    messagebox.showerror("Database Error", "Could not connect to database.")
                    return
                cursor = conn.cursor()
                cursor.execute("DELETE FROM books WHERE book_id = %s", (self.selected_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.clear_fields()
                self.load_books()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                if cursor: cursor.close()
                if conn and conn.is_connected(): conn.close()

    def clear_fields(self):
        self.selected_id = None
        self.id_entry.config(state="normal", bg="white")
        self.id_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.status_combo.set("Available")
        self.search_entry.delete(0, tk.END)
        if self.book_table.selection():
            self.book_table.selection_remove(self.book_table.selection())


if __name__ == "__main__":
    root = tk.Tk()
    app = BooksUI(root)
    root.mainloop()

