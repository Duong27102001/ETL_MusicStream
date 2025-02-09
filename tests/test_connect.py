import psycopg2
from psycopg2 import OperationalError

import sys
import os

# Thêm đường dẫn tới thư mục gốc của dự án
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DATABASE_CONFIG

def create_connection():
    try:
        # Thử kết nối đến cơ sở dữ liệu
        con = psycopg2.connect(**DATABASE_CONFIG)
        print("Kết nối thành công!")
        return con
    except OperationalError as e:
        # Xử lý lỗi kết nối
        print(f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None

# Gọi hàm để tạo kết nối
connection = create_connection()

# Kiểm tra kết nối
if connection:
    # Kết nối thành công, bạn có thể thực hiện các thao tác với cơ sở dữ liệu
    # ...
    connection.close()
else:
    # Kết nối thất bại, xử lý lỗi hoặc thử lại sau
    pass