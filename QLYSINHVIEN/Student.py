import psycopg2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="LAB5",
            user="postgres",
            password="123456"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới cơ sở dữ liệu: {e}")
        return None

conn = connect_db()
cursor = conn.cursor()

def refresh_list():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', tk.END, values=row)

def add_student():
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    major = entry_major.get()

    if not name or not age or not gender or not major:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin")
        return

    if not age.isdigit():
        messagebox.showwarning("Sai dữ liệu", "Tuổi phải là số")
        return

    cursor.execute("INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)",
                   (name, age, gender, major))
    conn.commit()
    refresh_list()

def update_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Lỗi", "Chọn sinh viên để cập nhật")
        return

    selected_id = tree.item(selected_item, "values")[0]
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    major = entry_major.get()

    if not name or not age or not gender or not major:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin")
        return

    if not age.isdigit():
        messagebox.showwarning("Sai dữ liệu", "Tuổi phải là số")
        return

    cursor.execute("UPDATE students SET name = %s, age = %s, gender = %s, major = %s WHERE id = %s",
                   (name, age, gender, major, selected_id))
    conn.commit()
    refresh_list()

def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Lỗi", "Chọn sinh viên để xóa")
        return

    selected_id = tree.item(selected_item, "values")[0]
    cursor.execute("DELETE FROM students WHERE id = %s", (selected_id,))
    conn.commit()
    refresh_list()

root = tk.Tk()
root.title("Quản lý Sinh Viên")

tk.Label(root, text="Tên:").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Tuổi:").grid(row=0, column=2)
entry_age = tk.Entry(root)
entry_age.grid(row=0, column=3, padx=15, pady= 15)

tk.Label(root, text="Giới tính:").grid(row=1, column=0)
entry_gender = tk.Entry(root)
entry_gender.grid(row=1, column=1)

tk.Label(root, text="Ngành học:").grid(row=1, column=2)
entry_major = tk.Entry(root)
entry_major.grid(row=1, column=3, padx= 10, pady= 10)

btn_add = tk.Button(root, text="Thêm sinh viên", command=add_student)
btn_add.grid(row=2, column=0,padx= 15, pady= 10)

btn_update = tk.Button(root, text="Cập nhật thông tin", command=update_student)
btn_update.grid(row=2, column=1)

btn_delete = tk.Button(root, text="Xóa sinh viên", command=delete_student)
btn_delete.grid(row=2, column=2)

btn_refresh = tk.Button(root, text="Tải lại danh sách", command=refresh_list)
btn_refresh.grid(row=2, column=3)

tree = ttk.Treeview(root, columns=("ID", "Tên", "Tuổi", "Giới tính", "Ngành"), show="headings", height=8)
tree.grid(row=3, column=0, columnspan=4)

tree.heading("ID", text="ID")
tree.heading("Tên", text="Tên")
tree.heading("Tuổi", text="Tuổi")
tree.heading("Giới tính", text="Giới tính")
tree.heading("Ngành", text="Ngành")

tree.column("ID", anchor=tk.CENTER, width=50)  # Ví dụ đặt chiều rộng cho cột ID
tree.column("Tên", anchor=tk.CENTER, width=150)
tree.column("Tuổi", anchor=tk.CENTER, width=50)
tree.column("Giới tính", anchor=tk.CENTER, width=100)
tree.column("Ngành", anchor=tk.CENTER, width=100)

root.resizable(False,False)

refresh_list()

root.mainloop()

conn.close()
