import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",         # كلمة المرور فارغة بشكل افتراضي في XAMPP
            database="library_db" # اسم قاعدة البيانات الموحد بينكم
        )
        return connection
    except mysql.connector.Error as e:
        print(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return None
conn = get_connection()
if conn and conn.is_connected():
    print("تم الاتصال بقاعدة البيانات بنجاح!")
    conn.close()
