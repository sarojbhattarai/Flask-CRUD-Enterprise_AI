from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.String(30), nullable=False)
    amount_due = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '%r %r %r %r %r' % (self.student_id, self.first_name, self.last_name, self.date_of_birth, self.amount_due)
    
# Path: app.py to create database
db.create_all()


# Path: app.py to get every students
@app.route('/student', methods=['GET'])
def get_items():
    students = Student.query.all()
    print(students)
    return render_template('student.html', students=students)

# Path: app.py to get single student
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return {'student_id': student.student_id, 'first_name': student.first_name, 'last_name': student.last_name, 'date_of_birth': student.date_of_birth, 'amount_due': student.amount_due}

# to post new student
@app.route('/student', methods=['POST'])
def create_student():
    student = Student(student_id = request.json['student_id'],first_name=request.json['first_name'], last_name=request.json['last_name'],date_of_birth=request.json['date_of_birth'],amount_due=request.json['amount_due'])
    db.session.add(student)
    db.session.commit()
    return {'student_id': student.date_of_birth}

# to update student
@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if 'student_id' in request.json:
        student.student_id = request.json['student_id']
    if 'first_name' in request.json:
        student.first_name = request.json['first_name']
    if 'last_name' in request.json:
        student.last_name = request.json['last_name']
    if 'date_of_birth' in request.json:
        student.date_of_birth=request.json['date_of_birth']
    if 'amount_due' in request.json:
        student.amount_due = request.json['amount_due']
    db.session.commit()
    return {'id': student.student_id}

# to delete student
@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return {'id': student.student_id}

if __name__ == '__main__':
    app.run(debug=True)

# homepage
@app.route('/student')
def student():
    return render_template('student.html')