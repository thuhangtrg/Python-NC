import psycopg2
from psycopg2 import sql

class DbConn:
    def __init__(self, database="qlynhanvien", table="nhan_vien", user="postgres", password="123456", host="localhost", port="5432"):
        self.database = database
        self.table = table  
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
        except Exception as ex:
            print(f"Error connecting to database: {ex}")
            raise ex
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def check_employee_exists(self, id):
        query = sql.SQL("SELECT * FROM {table} WHERE id = %s").format(
            table=sql.Identifier(self.table)
        )
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone() is not None

    def select(self, **conditions):
        try:
            query = "SELECT id, ten, tuoi, gioi_tinh, phong_ban FROM nhan_vien WHERE id = %s"
            self.cursor.execute(query, (conditions['id'],))
            rows = self.cursor.fetchall()

            results = []
            for row in rows:
                employee = {
                    'id': row[0],
                    'ten': row[1],
                    'tuoi': row[2],
                    'gioi_tinh': row[3],
                    'phong_ban': row[4]
                }
                results.append(employee)
            return results
        except Exception as e:
            print("Error fetching employee:", e)
            return []
        
    def get_employee_by_id(self, id):
        try:
            # Truy vấn bảng nhanvien với cột id
            sql = "SELECT * FROM nhan_vien WHERE id = %s"
            self.cursor.execute(sql, (id,))
            
            # Lấy tất cả kết quả (dù trong thực tế có thể chỉ có một kết quả duy nhất)
            result = self.cursor.fetchall()
            
            # Nếu không có kết quả, trả về None
            if not result:
                return None
            
            return result  # Trả về danh sách nhân viên tìm được
        except Exception as e:
            print(f"Error fetching employee: {e}")
            return None


    def insert(self, **kwargs):
        id = kwargs.get('id')
        if id and self.check_employee_exists(id):
            print(f"Nhân viên với ID {id} đã tồn tại.")
            return False
        
        try:
            columns = kwargs.keys()
            values = kwargs.values()
            query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
                table=sql.Identifier(self.table),
                fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            print("Insert thành công")
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error during insert: {ex}")
            return False

    def update(self, id, ten, tuoi, gioi_tinh, phong_ban):
        try:
            sql = """
            UPDATE nhanvien
            SET ten = %s, tuoi = %s, gioi_tinh = %s, phong_ban = %s
            WHERE id = %s
            """
            self.cursor.execute(sql, (ten, tuoi, gioi_tinh, phong_ban))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating employee: {e}")
            self.conn.rollback()
            return False


    def delete(self, **conditions):
        if not conditions:
            raise ValueError("No conditions provided for deletion.")

        id = conditions.get('id')
        if id and not self.check_employee_exists(id):
            print(f"Nhân viên với ID {id} không tồn tại.")
            return False

        conds = [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder()) for k in conditions.keys()]
        query = sql.SQL("DELETE FROM {table} WHERE {conds}").format(
            table=sql.Identifier(self.table),
            conds=sql.SQL(" AND ").join(conds)
        )
        self.cursor.execute(query, tuple(conditions.values()))
        self.conn.commit()
        print("Delete thành công")
        return True

    def check_login(self, username, password):
        query = sql.SQL("SELECT * FROM users WHERE username = %s AND password = %s")
        try:
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            if user:
                print("Login thành công")
                return True
            else:
                print("Sai tên đăng nhập hoặc mật khẩu")
                return False
        except Exception as ex:
            print(f"Error during login: {ex}")
            return False
