from flask import Flask, jsonify, request, render_template,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from fastapi import FastAPI

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from flask import Flask

# app = Flask(__name__)
app = FastAPI()

# 数据库连接配置
db = MySQLdb.connect(host='localhost', user='root', passwd='Lzx.19991116', db='student', charset='utf8')


@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.route('/',methods=['POST','GET'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if username == 'admin' and password == '123456':
#             return redirect(url_for('admin'))


@app.route('/index')
def index():
    if 'username' in session:

        return render_template('index.html')

    else:

        return redirect(url_for('login'))

# @app.route('/')
# def index():
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM your_table")  # 替换为您的实际查询
#     data = cursor.fetchall()
#     cursor.close()
#     return str(data)  # 以字符串形式返回数据以简单显示
#
# if __name__ == '__main__':
#     app.run(debug=True)


# 确保数据库连接在每次请求后关闭
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db'):
#         g.db.close()


#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Lzx.19991116@localhost/student.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
# # 学生模型
# class Student(db.Model):
#     uni = db.Column(db.String(100), primary_key=True)
#     name = db.Column(db.String(100))
#     schedule = db.Column(db.String(100))
#     interests = db.Column(db.String(100))
#
#     def to_dict(self):
#         return {
#             'uni': self.uni,
#             'name': self.name,
#             'schedule': self.schedule,
#             'interests': self.interests
#         }


# @app.route('/')
# def index():
#     return 'Hello World'

# @app.route('/login',methods=['POST','GET'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if username == 'admin' and password == '123456':
#             return redirect(url_for('admin'))


@app.route('/admin')
def admin():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM student_info")  # 确保这里是正确的表名
    students_data = cursor.fetchall()
    cursor.close()

    print(students_data)  # 添加这行来检查数据

    return render_template('admin.html', students=students_data)



@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        uni = request.form.get('uni')
        name = request.form.get('name')
        schedule = request.form.get('schedule')
        interests = request.form.get('interests')

        cursor = db.cursor()
        sql = "INSERT INTO students (id, name, schedule, interests) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (uni, name, schedule, interests))
        db.commit()
        cursor.close()

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/modify/<uni>', methods=['GET', 'POST'])
def modify_student(uni):
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        schedule = request.form.get('schedule')
        interests = request.form.get('interests')

        sql = "UPDATE students SET name=%s, schedule=%s, interests=%s WHERE id=%s"
        cursor.execute(sql, (name, schedule, interests, uni))
        db.commit()

        return redirect(url_for('index'))

    # GET 请求，获取学生当前信息
    sql = "SELECT * FROM students WHERE id=%s"
    cursor.execute(sql, (uni,))
    student = cursor.fetchone()
    cursor.close()

    return render_template('modify.html', student=student)

@app.route('/delete/<uni>', methods=['GET'])
def delete_student(uni):
    cursor = db.cursor()
    sql = "DELETE FROM students WHERE id=%s"
    cursor.execute(sql, (uni,))
    db.commit()
    cursor.close()

    return redirect(url_for('index'))


# 添加或更新学生信息
@app.route('/student/<int:student_id>', methods=['POST'])
def add_or_update_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if not student:
        student = Student(id=student_id, name=data['name'], schedule=data['schedule'], interests=data['interests'])
        db.session.add(student)
    else:
        student.name = data['name']
        student.schedule = data['schedule']
        student.interests = data['interests']
    db.session.commit()
    return jsonify({'message': 'Student added/updated successfully'}), 200

# 获取学生信息
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student:
        return jsonify(student.to_dict()), 200
    else:
        return jsonify({'message': 'Student not found'}), 404

# 程序入口

if __name__ == '__main__':
    app.run(debug=True)
