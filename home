import tkinter as tk
from tkinter import ttk
from database import get_connection


bg_color = "#F5EBE0"
card_bg = "#EEDDC3"
btn_color = "#5C4033"
text_color = "#3E2723"
sub_text = "#7A6858"

def get_stats():

    conn = get_connection()

    total_b, total_m, total_br = 0, 0, 0

    if conn:
        cursor = None

        try:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM books")
            total_b = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM member")
            total_m = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM borrow WHERE status='Active'"
            )
            total_br = cursor.fetchone()[0]

        except Exception as e:
            print("Error getting dashboard statistics:", e)

        finally:
            if cursor:
                cursor.close()

            if conn.is_connected():
                conn.close()

    return total_b, total_m, total_br


def refresh_home_stats():

    b_count, m_count, br_count = get_stats()

    lbl_books_val.config(text=str(b_count))
    lbl_members_val.config(text=str(m_count))
    lbl_borrow_val.config(text=str(br_count))



def create_home_page(notebook):

    global lbl_books_val
    global lbl_members_val
    global lbl_borrow_val

    # Home tab
    tab_home = tk.Frame(notebook, bg=bg_color)

    notebook.add(tab_home, text=" Home ")


    tk.Label(
        tab_home,
        text="BOOKHAVEN",
        font=("Arial", 22, "bold"),
        bg=bg_color,
        fg=text_color
    ).place(x=50, y=40)

    tk.Label(
        tab_home,
        text="A quiet place for every story, reader, and treasured volume.",
        font=("Arial", 12),
        bg=bg_color,
        fg=sub_text
    ).place(x=50, y=80)


    card_h1 = tk.Frame(
        tab_home,
        bg=card_bg,
        width=300,
        height=130,
        relief="solid",
        bd=1
    )

    card_h1.place(x=50, y=140)

    tk.Label(
        card_h1,
        text="Total Books",
        font=("Arial", 11, "bold"),
        bg=card_bg,
        fg=sub_text
    ).place(x=20, y=20)

    lbl_books_val = tk.Label(
        card_h1,
        text="0",
        font=("Arial", 24, "bold"),
        bg=card_bg,
        fg=text_color
    )

    lbl_books_val.place(x=20, y=55)

  

    card_h2 = tk.Frame(
        tab_home,
        bg=card_bg,
        width=300,
        height=130,
        relief="solid",
        bd=1
    )

    card_h2.place(x=380, y=140)

    tk.Label(
        card_h2,
        text="Total Borrowers",
        font=("Arial", 11, "bold"),
        bg=card_bg,
        fg=sub_text
    ).place(x=20, y=20)

    lbl_members_val = tk.Label(
        card_h2,
        text="0",
        font=("Arial", 24, "bold"),
        bg=card_bg,
        fg=text_color
    )

    lbl_members_val.place(x=20, y=55)

    

    card_h3 = tk.Frame(
        tab_home,
        bg=card_bg,
        width=300,
        height=130,
        relief="solid",
        bd=1
    )

    card_h3.place(x=710, y=140)

    tk.Label(
        card_h3,
        text="Active Borrowings",
        font=("Arial", 11, "bold"),
        bg=card_bg,
        fg=sub_text
    ).place(x=20, y=20)

    lbl_borrow_val = tk.Label(
        card_h3,
        text="0",
        font=("Arial", 24, "bold"),
        bg=card_bg,
        fg=text_color
    )

    lbl_borrow_val.place(x=20, y=55)

    

    btn_refresh_home = ttk.Button(
        tab_home,
        text="Refresh Dashboard Stats",
        command=refresh_home_stats,
        style="Custom.TButton"
    )

    btn_refresh_home.place(x=50, y=300)

    # Load statistics when Home page is created
    refresh_home_stats()

    return tab_home


if __name__ == "__main__":

    root = tk.Tk()
    root.title("BookHaven - Library Management System")
    root.geometry("1100x750")
    root.configure(bg=bg_color)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.TButton",
        background=btn_color,
        foreground="white",
        font=("Arial", 9, "bold")
    )

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    create_home_page(notebook)

    root.mainloop()
    
