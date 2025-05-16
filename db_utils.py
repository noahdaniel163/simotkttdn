import pyodbc
from db_config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD

# Hàm chuẩn hóa chuỗi cho tìm kiếm tương đối (không phân biệt hoa thường, loại bỏ khoảng trắng thừa)
def normalize_str(s):
    if s is None:
        return None
    return ''.join(s.lower().split())

def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"
    )
    return pyodbc.connect(conn_str)

def search_tktt_tochuc(**kwargs):
    query = "SELECT * FROM TKTT_TOCHUC WHERE 1=1"
    params = []
    for field, value in kwargs.items():
        if value is not None and value != "":
            # Tìm kiếm tương đối: loại bỏ khoảng trắng, không phân biệt hoa thường
            query += f" AND LOWER(REPLACE({field}, ' ', '')) LIKE ?"
            params.append(f"%{normalize_str(value)}%")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results
