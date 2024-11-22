from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, request
from controller import DbConn  # Giả định DbConn nằm trong controller.py
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Cần có để hiển thị thông báo lỗi

# Hàm xử lý trang đăng nhập
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Kiểm tra đăng nhập
        with DbConn() as db:
            if db.check_login(username, password):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Sai tên đăng nhập hoặc mật khẩu")
    
    return render_template('login.html') 

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Sử dụng hàm get_top_employees từ controller
    from controller import get_top_employees
    employees = get_top_employees()  # Gọi hàm để lấy danh sách nhân viên
    
    return render_template('dashboard.html', employees=employees)  # Truyền dữ liệu vào template


# thêm
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        data = {
            'id': request.form['id'],
            'ten': request.form['ten'],
            'tuoi': request.form['tuoi'],
            'gioi_tinh': request.form['gioi_tinh'],
            'phong_ban': request.form['phong_ban']
        }
        with DbConn() as db:
            if db.insert(**data):
                flash("Thêm nhân viên thành công")
            else: 
                flash("Nhân viên đã tồn tại hoặc lỗi xảy ra")
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html')

@app.route('/edit_employee', methods=['GET', 'POST'])

def edit_employee():
    employee = None
    if request.method == 'POST' and 'search' in request.form:
        # Lấy ID nhân viên người dùng nhập vào
        emp_id = request.form['id']
        
        # Tìm nhân viên từ cơ sở dữ liệu
        with DbConn() as db:
            # Tìm nhân viên theo ID
            employee = db.select(id=emp_id)  # Tìm nhân viên theo ID
            if employee:
                employee = employee[0]  # Chỉ lấy nhân viên đầu tiên từ kết quả
            else:
                flash("Nhân viên không tồn tại")
                return redirect(url_for('edit_employee'))  # Quay lại trang sửa nếu không tìm thấy nhân viên

    elif request.method == 'POST' and 'update' in request.form:
            # Khi người dùng gửi thông tin cập nhật
            employee_id = request.form['id']
            name = request.form['ten']
            age = request.form['tuoi']
            gender = request.form['gioi_tinh']
            department = request.form['phong_ban']
            
            # Cập nhật thông tin nhân viên trong cơ sở dữ liệu
            with DbConn() as db:
                # Sử dụng phương thức update_employee của DbConn để cập nhật thông tin
                if db.update(employee_id, name, age, gender, department):
                    flash("Cập nhật nhân viên thành công", "success")
                    return redirect(url_for('edit_employee'))  # Quay lại trang chỉnh sửa sau khi thành công
                else:
                    flash("Lỗi cập nhật nhân viên", "error")
                    return redirect(url_for('edit_employee'))  # Quay lại trang sửa nếu có lỗi

    return render_template('edit_employee.html', employee=employee)


# xóa
@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        with DbConn() as db:
            if db.delete(id=employee_id):
                flash("Xóa nhân viên thành công")
            else:
                flash("Nhân viên không tồn tại")
        return redirect(url_for('dashboard'))
    return render_template('delete_employee.html')



# tìm
@app.route('/search', methods=['GET', 'POST'])
def search_employee():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        with DbConn() as db:
            results = db.select(id=keyword)
    return render_template('search_employee.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
