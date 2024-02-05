import random
from flask import Flask, render_template, request, redirect, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    group = db.Column(db.Integer)

    def __init__(self, name, gender, group=None):
        self.name = name
        self.gender = gender
        self.group = group

#student = Student(name, gender)

@app.route('/')
def index():
    students = Student.query.all()
    group1 = Student.query.filter_by(group=1).all()
    group2 = Student.query.filter_by(group=2).all()
    group3 = Student.query.filter_by(group=3).all()
    group4 = Student.query.filter_by(group=4).all()
    return render_template('index.html', students=students, group1=group1, group2=group2, group3=group3, group4=group4)


@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['student_name']
    gender = request.form['student_gender']
    student = Student(name,gender)
    #student = Student(gender)
    db.session.add(student)
    db.session.commit()
    return redirect('/')


@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        student.name = request.form['student_name']
        student.gender = request.form['student_gender']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', student=student)


@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')


@app.route('/assign_group/<int:student_id>', methods=['POST'])
def assign_group(student_id):
    student = Student.query.get(student_id)
    group_number = random.randint(1, 4)
    student.group = group_number
    db.session.commit()
    return jsonify({'success': True, 'studentName': student.name, 'groupNumber': group_number})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)