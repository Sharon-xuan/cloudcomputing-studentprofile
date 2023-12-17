from flask import Flask, jsonify, request, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # 学生模型
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     schedule = db.Column(db.String(256))  # 或者使用更复杂的数据类型
#     interests = db.Column(db.String(256)) # 根据需要调整字段类型和长度

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'schedule': self.schedule,
    #         'interests': self.interests
    #     }



# 学生模型
# class Student:
#     def __init__(self, id, name, schedule, interests):
#         self.id = id
#         self.name = name
#         self.schedule = schedule
#         self.interests = interests

# @app.route('/')
# def index():
#     return 'Hello World'

@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123456':
            return redirect(url_for('admin'))

# 示例数据存储（在实际应用中应该替换为数据库）
students = [
    {'uni':'zl3218','name':'Zixuan Li','schedule':'Monday','interests':'cloud computing'},
    {'uni':'yf2633','name':'Yuxiao Fei','schedule':'Monday','interests':'cloud computing'},
    {'uni':'rw2959','name':'Ruobing Wang','schedule':'Monday','interests':'cloud computing'},
    {'uni':'ym2876','name':'Philip Ma','schedule':'Monday','interests':'cloud computing'},
    {'uni':'lz2933','name':'Lanyue Zhang','schedule':'Monday','interests':'cloud computing'},
    {'uni':'qf2172','name':'Quan Fang','schedule':'Monday','interests':'cloud computing'}
]
@app.route('/admin')
def admin():
    return render_template('admin.html',students=students)


@app.route('/add',methods=['POST','GET'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        uni = request.form.get('uni')
        name = request.form.get('name')
        schedule = request.form.get('schedule')
        interests = request.form.get('interests')
        students.append({'uni':uni,'name':name,'schedule':schedule,'interests':interests})
        return redirect(url_for('admin'))

@app.route('/modify/<uni>', methods=['GET', 'POST'])
def modify(uni):
    student_to_modify = next((student for student in students if student['uni'] == uni), None)

    if request.method == 'POST':
        name = request.form['name']
        schedule = request.form['schedule']
        interests = request.form['interests']

        if student_to_modify:
            student_to_modify['name'] = name
            student_to_modify['schedule'] = schedule
            student_to_modify['interests'] = interests
            return redirect(url_for('admin'))
        else:
            return 'Student not found', 404

    if student_to_modify:
        return render_template('modify.html', student=student_to_modify)
    else:
        return 'Student not found', 404

# @app.route('/modify/<uni>', methods=['GET', 'POST'])
# def modify(uni):
#     stu_id = request.args.get('uni')
#
#     if request.method == 'POST':
#         uni = request.form.get('uni')
#         name = request.form.get('name')  # 将此行移到这里
#         schedule = request.form.get('schedule')
#         interests = request.form.get('interests')
#         for student in students:
#             if student['uni'] == uni:
#                 student['name'] = name
#                 student['schedule'] = schedule
#                 student['interests'] = interests
#         return redirect(url_for('admin'))
#
#     for student in students:
#         if student['uni'] == stu_id:
#             return render_template('modify.html', student=student)
#
#     # 如果没有找到学生，可以重定向到其他页面或显示错误消息
#     return 'Student not found', 404  # 添加这行

@app.route('/delete', methods=['GET'])
def delete_student():
    stu_uni = request.args.get('uni')
    global students  # 如果您要修改它，需要声明 students 为全局变量
    students = [student for student in students if student['uni'] != stu_uni]
    return redirect(url_for('admin'))

# @app.route('/delete',methods=['GET'])
# def delete_student():
#     stu_uni = request.args.get('uni')
#     for student in students:
#         if student['uni'] == stu_uni:
#             students.remove(student)
#     return redirect(url_for('admin'))


# # 添加或更新学生信息
# @app.route('/student/<int:student_id>', methods=['POST'])
# def add_or_update_student(student_id):
#     data = request.json
#     student = Student.query.get(student_id)
#     if not student:
#         student = Student(id=student_id, name=data['name'], schedule=data['schedule'], interests=data['interests'])
#         db.session.add(student)
#     else:
#         student.name = data['name']
#         student.schedule = data['schedule']
#         student.interests = data['interests']
#     db.session.commit()
#     return jsonify({'message': 'Student added/updated successfully'}), 200
#
# # 获取学生信息
# @app.route('/student/<int:student_id>', methods=['GET'])
# def get_student(student_id):
#     student = Student.query.get(student_id)
#     if student:
#         return jsonify(student.to_dict()), 200
#     else:
#         return jsonify({'message': 'Student not found'}), 404

# 程序入口
if __name__ == '__main__':
    app.run(debug=True)
