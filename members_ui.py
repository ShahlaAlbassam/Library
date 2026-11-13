import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from database import get_connection


class MembersUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Book Heaven - Members Management")
        self.root.geometry("1100x750")

        self.bg_color = "#F5EBE0"
        self.btn_color = "#5C4033"
        self.text_color = "#3E2723"
        self.sub_text = "#7A6858"

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
            text="MEMBERS MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w", padx=20, pady=10)

        input_frame = tk.LabelFrame(
            root,
            text="MEMBER DETAILS",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=10
        )
        input_frame.pack(fill="x", padx=20, pady=5)

        # الصف الأول: Name و Email
        tk.Label(input_frame, text="Name *:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=6, sticky="w")
        self.name_entry = tk.Entry(input_frame, width=28, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.name_entry.grid(row=0, column=1, padx=5, pady=6)

        tk.Label(input_frame, text="Email *:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=6, sticky="w")
        self.email_entry = tk.Entry(input_frame, width=28, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.email_entry.grid(row=0, column=3, padx=5, pady=6)

        # الصف الثاني: Phone
        tk.Label(input_frame, text="Phone *:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=6, sticky="w")
        self.phone_entry = tk.Entry(input_frame, width=28, bg="white", fg=self.text_color, relief="solid", bd=1)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=6)

        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="+ Add Member", command=self.add_member, style="Custom.TButton").grid(row=0, column=0, padx=5, ipadx=5, ipady=3)
        ttk.Button(button_frame, text="Update Member", command=self.update_member, style="Custom.TButton").grid(row=0, column=1, padx=5, ipadx=5, ipady=3)
        ttk.Button(button_frame, text="Delete Member", command=self.delete_member, style="Danger.TButton").grid(row=0, column=2, padx=5, ipadx=5, ipady=3)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_fields, style="Gray.TButton").grid(row=0, column=3, padx=5, ipadx=5, ipady=3)

        table_frame = tk.Frame(root, bg=self.bg_color)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Email", "Phone")
        self.member_table = ttk.Treeview(table_frame, columns=columns, show="headings")

        for column in columns:
            self.member_table.heading(column, text=column)

        self.member_table.column("ID", width=80, anchor="center")
        self.member_table.column("Name", width=220)
        self.member_table.column("Email", width=220)
        self.member_table.column("Phone", width=160, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.member_table.yview)
        self.member_table.configure(yscrollcommand=scrollbar.set)

        self.member_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.member_table.bind("<<TreeviewSelect>>", self.select_member)
        self.load_members()

    def load_members(self):
        for item in self.member_table.get_children():
            self.member_table.delete(item)
        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Member_id, Member_name, email, phone FROM member")
                for row in cursor.fetchall():
                    self.member_table.insert("", "end", values=row)
        except Exception as e:
            print("Error loading members:", e)
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def add_member(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not email or not phone:
            messagebox.showwarning("Missing Information", "Please fill in all fields!")
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO member (Member_name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
                conn.commit()
                messagebox.showinfo("Success", "Member added successfully!")
                self.clear_fields()
                self.load_members()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def select_member(self, event):
        selected = self.member_table.selection()
        if selected:
            values = self.member_table.item(selected[0], "values")
            self.selected_id = values[0]  # حفظ الـ ID للتعديل أو الحذف

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])

            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])

            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, values[3])

    def update_member(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Please select a member from the table first.")
            return
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not email or not phone:
            messagebox.showwarning("Missing Information", "Please fill in all fields!")
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE member SET Member_name = %s, email = %s, phone = %s WHERE Member_id = %s", (name, email, phone, self.selected_id))
                conn.commit()
                messagebox.showinfo("Success", "Member updated successfully!")
                self.clear_fields()
                self.load_members()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def delete_member(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Please select a member from the table first.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?"):
            conn = None
            cursor = None
            try:
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM member WHERE Member_id = %s", (self.selected_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Member deleted successfully!")
                    self.clear_fields()
                    self.load_members()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if cursor: cursor.close()
                if conn and conn.is_connected(): conn.close()

    def clear_fields(self):
        self.selected_id = None
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        if self.member_table.selection():
            self.member_table.selection_remove(self.member_table.selection())


if __name__ == "__main__":
    root = tk.Tk()
    app = MembersUI(root)
    root.mainloop()

