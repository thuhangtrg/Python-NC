import psycopg2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Kết nối đến cơ sở dữ liệu PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="qlynhanvien",
            user="postgres",
            password="123456"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới cơ sở dữ liệu: {e}")
        return None

conn = connect_db()
cursor = conn.cursor()

# Hàm tải lại danh sách nhân viên
def refresh_list():
    try:
        cursor.execute("SELECT * FROM nhan_vien")
        rows = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert('', tk.END, values=row)
        messagebox.showinfo("Thành công", "Tải lại danh sách thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải lại danh sách: {e}")

# Hàm thêm nhân viên mới
def add_employee():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    department = entry_department.get()

    if not name or not age or not gender or not department:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin")
        return

    if not age.isdigit():
        messagebox.showwarning("Sai dữ liệu", "Tuổi phải là số")
        return

    try:
        cursor.execute("INSERT INTO nhan_vien (ten, tuoi, gioi_tinh, phong_ban) VALUES (%s, %s, %s, %s)",
                       (name, age, gender, department))
        conn.commit()
        refresh_list()
        messagebox.showinfo("Thành công", "Thêm nhân viên thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm nhân viên: {e}")

# Hàm cập nhật thông tin nhân viên
def update_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Lỗi", "Chọn nhân viên để cập nhật")
        return

    selected_id = tree.item(selected_item, "values")[0]
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    department = entry_department.get()

    if not name or not age or not gender or not department:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin")
        return

    if not age.isdigit():
        messagebox.showwarning("Sai dữ liệu", "Tuổi phải là số")
        return

    try:
        cursor.execute("UPDATE nhan_vien SET ten = %s, tuoi = %s, gioi_tinh = %s, phong_ban = %s WHERE id = %s",
                       (name, age, gender, department, selected_id))
        conn.commit()
        refresh_list()
        messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật nhân viên: {e}")

# Hàm xóa nhân viên
def delete_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Lỗi", "Chọn nhân viên để xóa")
        return

    selected_id = tree.item(selected_item, "values")[0]

    try:
        cursor.execute("DELETE FROM nhan_vien WHERE id = %s", (selected_id,))
        conn.commit()
        refresh_list()
        messagebox.showinfo("Thành công", "Xóa nhân viên thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa nhân viên: {e}")

# Giao diện người dùng với Tkinter
root = tk.Tk()
root.title("Quản lý Nhân Viên")

tk.Label(root, text="Tên:").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, columnspan=2)

tk.Label(root, text="Tuổi:").grid(row=1, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, padx=15, pady=15, columnspan=2)

# Sử dụng radio button cho giới tính
gender_var = tk.StringVar(value="Nam")
tk.Label(root, text="Giới tính:").grid(row=2, column=0)
radio_male = tk.Radiobutton(root, text="Nam", variable=gender_var, value="Nam")
radio_male.grid(row=2, column=1)
radio_female = tk.Radiobutton(root, text="Nữ", variable=gender_var, value="Nữ")
radio_female.grid(row=2, column=2)

tk.Label(root, text="Phòng ban:").grid(row=3, column=0)
entry_department = tk.Entry(root)
entry_department.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

# Các nút thêm, cập nhật, xóa, và tải lại danh sách
btn_add = tk.Button(root, text="Thêm nhân viên", command=add_employee)
btn_add.grid(row=4, column=0, padx=15, pady=10)

btn_update = tk.Button(root, text="Cập nhật thông tin", command=update_employee)
btn_update.grid(row=4, column=1)

btn_delete = tk.Button(root, text="Xóa nhân viên", command=delete_employee)
btn_delete.grid(row=4, column=2)

btn_refresh = tk.Button(root, text="Tải lại danh sách", command=refresh_list)
btn_refresh.grid(row=4, column=3)

# Bảng hiển thị danh sách nhân viên
tree = ttk.Treeview(root, columns=("ID", "Tên", "Tuổi", "Giới tính", "Phòng ban"), show="headings", height=8)
tree.grid(row=5, column=0, columnspan=4)

# Đặt tiêu đề cho các cột
tree.heading("ID", text="ID")
tree.heading("Tên", text="Tên")
tree.heading("Tuổi", text="Tuổi")
tree.heading("Giới tính", text="Giới tính")
tree.heading("Phòng ban", text="Phòng ban")

# Điều chỉnh kích thước các cột
tree.column("ID", anchor=tk.CENTER, width=50)
tree.column("Tên", anchor=tk.CENTER, width=150)
tree.column("Tuổi", anchor=tk.CENTER, width=50)
tree.column("Giới tính", anchor=tk.CENTER, width=100)
tree.column("Phòng ban", anchor=tk.CENTER, width=100)

# Không cho phép thay đổi kích thước cửa sổ
root.resizable(False, False)

# Tải lại danh sách nhân viên từ cơ sở dữ liệu
refresh_list()

# Chạy giao diện người dùng
root.mainloop()

# Đóng kết nối sau khi đóng ứng dụng
conn.close()
