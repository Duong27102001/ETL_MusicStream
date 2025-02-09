import sys
import os
# Thêm đường dẫn tới thư mục gốc của dự án
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psycopg2
from config.config import DATABASE_CONFIG
from database.sql_queries import create_table_queries, drop_table_queries

def create_database_musicStream():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    #xoá bảng nếu tồn tại
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
        
    #tạo bảng trong databse
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    conn.close()
    