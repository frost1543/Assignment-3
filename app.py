from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Student('{self.first_name}', '{self.last_name}', '{self.dob}', '{self.amount_due}')"

db.create_all()

@app.route('/')
def index():
    return "Welcome to the Student API!"

@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
        amount_due=data['amount_due']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully!'}), 201

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    output = []
    for student in students:
        student_data = {
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'amount_due': student.amount_due
        }
        output.append(student_data)
    return jsonify({'students': output})

@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student:
        student_data = {
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'amount_due': student.amount_due
        }
        return jsonify(student_data)
    else:
        return jsonify({'message': 'Student not found'}), 404

@app.route('/student/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get(student_id)
    if student:
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
        student.amount_due = data['amount_due']
        db.session.commit()
        return jsonify({'message': 'Student updated successfully!'})
    else:
        return jsonify({'message': 'Student not found'}), 404

@app.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully!'})
    else:
        return jsonify({'message': 'Student not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
