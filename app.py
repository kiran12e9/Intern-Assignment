from datetime import datetime
from enum import Enum
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/rkira/Desktop/Student.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class StudentDetails(db.Model):
    __tablename__ = 'StudentDetails'
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    roll_no = db.Column(db.String(50), primary_key=True)
    dob = db.Column(db.Date)
    year = db.Column(db.String(50))
    branch = db.Column(db.String(50))
    college = db.Column(db.String(100))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            roll_no = request.form['rollno']
            existing_student = StudentDetails.query.filter_by(roll_no=roll_no).first()
            if existing_student:
                return render_template("index.html",message="Student with Roll No already exists!!")
            name = request.form['name']
            surname = request.form['surname']
            dob_str = request.form['dob']
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            year = request.form['year']
            branch = request.form['branch']
            college = request.form['collegename']
        except:
            return render_template("index.html",message="Error in accessing form details")
        try:
            student = StudentDetails(roll_no=roll_no, name=name, surname=surname, dob=dob, year=year, branch=branch, college=college)
            db.session.add(student)
            db.session.commit()
            return render_template("index.html", message="Successfully added student details")
        except Exception as e:
            return render_template("index.html", message=str(e))
    else:
        return render_template("index.html")

@app.route('/getdata', methods=['GET'])
def getdata():
    try:
        students = StudentDetails.query.all()
        return render_template("students.html", students=students)
    except Exception as e:
        return render_template("students.html", message="Error in fetching the details from the database")
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()       
    app.run(debug=True)

