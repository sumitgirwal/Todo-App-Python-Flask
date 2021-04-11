from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todoapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

 

class Task(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = True)
	created_date = db.Column(db.DateTime, default = datetime.utcnow)
	def __repr__(self) -> str:
		return f"{self.id} - {self.title}"


@app.route('/tasks', methods = ['GET', 'POST'])
def tasks():
	#create task
	#db.create_all()
	if request.method == 'POST':
		title = request.form['title']
		task = Task(title = title)
		db.session.add(task)
		db.session.commit()

	#show tasks		
	task_list = Task.query.all()
	return render_template('index.html', task_list = task_list)				


@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):	
	task = Task.query.filter_by(id = id).first()
	return redirect('/tasks')					

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):	
	task = Task.query.filter_by(id = id).first()
	db.session.delete(task)
	db.session.commit()
	return redirect('/tasks')				

if __name__ == '__main__':
	app.run(debug = True, port = 8000)





