from model import DbConn
import psycopg2

class EmployeeController:
    def __init__(self, treeview):
        self.treeview = treeview

    def load_all_employees(self):
        # Sử dụng DbConn để lấy dữ liệu nhân viên từ database
        with DbConn() as db:
            results = db.select()  # Lấy tất cả nhân viên từ bảng
            # Xóa tất cả nội dung hiện tại trong Treeview
            self.treeview.delete(*self.treeview.get_children())
            # Chèn từng dòng kết quả vào Treeview
            for row in results:
                self.treeview.insert('', 'end', values=row)

    def insert_employee(self, **employee_data):
        with DbConn() as db:
            success = db.insert(**employee_data)
            return success

    def update_employee(self, update_data, **conditions):
        with DbConn() as db:
            success = db.update(update_data, **conditions)
            return success

    def delete_employee(self, **conditions):
        with DbConn() as db:
            success = db.delete(**conditions)
            return success

def get_top_employees():
    conn = psycopg2.connect(
        host="localhost",
        database="qlynhanvien",  # Cập nhật tên cơ sở dữ liệu
        user="postgres",
        password="123456"
    )
    cursor = conn.cursor()
    query = """
        SELECT id, ten, tuoi, gioi_tinh, phong_ban
        FROM nhan_vien
        ORDER BY id
        LIMIT 10;
    """
    cursor.execute(query)
    employees = cursor.fetchall()  # Lấy tất cả kết quả
    cursor.close()
    conn.close()
    return employees
