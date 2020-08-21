from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pa$$1234@localhost/Feedback'
else:
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vcqevekamqmnlz:4da4e7ac2a7d63c4a17c2fcf064f12527d04ab34d42f83c7433498d589b08be7@ec2-54-156-121-142.compute-1.amazonaws.com:5432/d4q08147755960'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
	__tablename__ = 'feedback'
	id = db.Column(db.Integer, primary_key=True)
	student = db.Column(db.String(200), unique=True)
	Professor = db.Column(db.String(200))
	rating = db.Column(db.Integer)
	comments = db.Column(db.Text())
    	
	def __init__(self, student, Professor, rating, comments):
		self.student = student
		self.Professor = Professor
		self.rating = rating
		self.comments = comments

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/submit', methods=['POST'])
def submit():
	if request.method == 'POST':
		student = request.form['Student']
		Professor = request.form['Professor']
		rating = request.form['rating']
		comments = request.form['comments']
		#print(student,Professor,rating,comments)
		if student == '' or Professor == '':
			return render_template('index.html',message = 'Please enter required fields')
		if db.session.query(Feedback).filter(Feedback.student == student).count() == 0:
			data = Feedback(student, Professor, rating, comments)
			db.session.add(data)
			db.session.commit()
			#send_mail(student, Professor, rating, comments)
			return render_template('success.html')
		return render_template('index.html', message='You have already submitted feedback')
	
if __name__ == '__main__':
	app.run()
