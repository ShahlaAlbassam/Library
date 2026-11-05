import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",         
            database="library_db"  
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Something wrong with the data base: {e}")
        return None
conn = get_connection()
if conn and conn.is_connected():
    print("Data base connected successfuly")
    conn.close()
