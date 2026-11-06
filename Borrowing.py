import customtkinter as ctk
import mysql.connector
from datetime import datetime
from database import get_connection

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")

class BorrowingsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BookHaven - Borrowings Management")
        self.geometry("1100x650")
        self.configure(fg_color="#F4EFEA")

        # Main Title
        self.title_label = ctk.CTkLabel(
            self,
            text="BORROWINGS",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="#3D291D"
        )
        self.title_label.place(x=50, y=40)

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Issue books and monitor active borrowing records.",
            font=ctk.CTkFont(family="Arial", size=13),
            text_color="#7A6858"
        )
        self.subtitle_label.place(x=50, y=75)

        # Issue A Book Form Frame
        self.form_frame = ctk.CTkFrame(self, width=400, height=480, corner_radius=15, fg_color="#FFFFFF")
        self.form_frame.place(x=50, y=120)

        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="ISSUE A BOOK",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#3D291D"
        )
        self.form_title.place(x=30, y=25)

        # Select Member Dropdown
        self.member_label = ctk.CTkLabel(self.form_frame, text="Select member *", font=ctk.CTkFont(size=12), text_color="#555")
        self.member_label.place(x=30, y=70)

        self.members_list = self.fetch_members()
        self.member_dropdown = ctk.CTkComboBox(
            self.form_frame,
            values=self.members_list if self.members_list else ["No members found"],
            width=340, height=35,
            fg_color="#F9F9F9", border_color="#E0D6CE"
        )
        self.member_dropdown.place(x=30, y=95)

        # Select Book Dropdown
        self.book_label = ctk.CTkLabel(self.form_frame, text="Select book *", font=ctk.CTkFont(size=12), text_color="#555")
        self.book_label.place(x=30, y=150)

        self.books_list = self.fetch_books()
        self.book_dropdown = ctk.CTkComboBox(
            self.form_frame,
            values=self.books_list if self.books_list else ["No books found"],
            width=340, height=35,
            fg_color="#F9F9F9", border_color="#E0D6CE"
        )
        self.book_dropdown.place(x=30, y=175)

        # Date Entries
        self.issue_date_label = ctk.CTkLabel(self.form_frame, text="Issue date", font=ctk.CTkFont(size=12), text_color="#555")
        self.issue_date_label.place(x=30, y=230)

        self.issue_date_entry = ctk.CTkEntry(self.form_frame, width=160, height=35, fg_color="#F9F9F9")
        self.issue_date_entry.place(x=30, y=255)
        self.issue_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.due_date_label = ctk.CTkLabel(self.form_frame, text="Due date", font=ctk.CTkFont(size=12), text_color="#555")
        self.due_date_label.place(x=210, y=230)

        self.due_date_entry = ctk.CTkEntry(self.form_frame, width=160, height=35, fg_color="#F9F9F9")
        self.due_date_entry.place(x=210, y=255)
        self.due_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Issue Button
        self.issue_button = ctk.CTkButton(
            self.form_frame,
            text="Issue Book →",
            command=self.issue_book_action,
            width=340, height=40,
            fg_color="#4A3323", hover_color="#3D291D",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.issue_button.place(x=30, y=330)

        # Active Borrowings Table Frame
        self.table_frame = ctk.CTkFrame(self, width=580, height=480, corner_radius=15, fg_color="#FFFFFF")
        self.table_frame.place(x=470, y=120)

        self.table_title = ctk.CTkLabel(
            self.table_frame,
            text="ACTIVE BORROWINGS",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="#3D291D"
        )
        self.table_title.place(x=25, y=25)

        # Table Header Frame
        self.header_frame = ctk.CTkFrame(self.table_frame, width=530, height=30, fg_color="#F9F5F0", corner_radius=6)
        self.header_frame.place(x=25, y=65)

        headers = ["REF", "MEMBER", "BOOK TITLE", "ISSUED", "DUE DATE", "STATUS"]
        x_positions = [10, 80, 180, 310, 390, 470]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.header_frame, text=h, font=ctk.CTkFont(size=10, weight="bold"), text_color="#7A6858").place(x=x_positions[i], y=5)

        # Scrollable Frame for Active Borrowings Records
        self.records_scroll = ctk.CTkScrollableFrame(self.table_frame, width=515, height=350, fg_color="#FFFFFF")
        self.records_scroll.place(x=25, y=105)

        self.load_active_borrowings()

    def fetch_members(self):
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

    def fetch_books(self):
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

    def load_active_borrowings(self):
        for widget in self.records_scroll.winfo_children():
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
                    lbl = ctk.CTkLabel(
                        self.records_scroll,
                        text=row_text,
                        font=ctk.CTkFont(size=11),
                        text_color="#3D291D",
                        anchor="w"
                    )
                    lbl.pack(fill="x", padx=5, pady=4)

            except Exception as e:
                print(f"Error loading records: {e}")

    def issue_book_action(self):
        selected_member = self.member_dropdown.get()
        selected_book = self.book_dropdown.get()
        issue_date = self.issue_date_entry.get()
        due_date = self.due_date_entry.get()

        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO borrow (member_name, book_title, borrow_date, due_date, status) VALUES (%s, %s, %s, %s, %s)"
                values = (selected_member, selected_book, issue_date, due_date, "Active")
                cursor.execute(query, values)
                conn.commit()
                conn.close()
                print("Book issued successfully!")
                self.load_active_borrowings() # Refresh table records
            except Exception as e:
                print(f"Error issuing book: {e}")


if __name__ == "__main__":
    app = BorrowingsApp()
    app.mainloop()
