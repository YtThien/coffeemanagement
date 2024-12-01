import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
print(sys.path)
import MySQLdb as mdb


def create_connection():
    conn = None
    try:
        conn = mdb.connect('localhost', 'root', '', 'cafe')
        if conn:
            print("Kết nối thành công")
    except mdb.Error as e:
        print(f"Lỗi: '{e}'")
        import traceback
        traceback.print_exc()
    return conn


# Kiểm tra kết nối
connection = create_connection()
if connection:
    # Kết nối thành công, bạn có thể tiếp tục sử dụng đối tượng connection
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    db_version = cursor.fetchone()
    print(f"Phiên bản MySQL: {db_version[0]}")
    cursor.close()
    connection.close()
else:
    print("Không thể kết nối tới cơ sở dữ liệu")
