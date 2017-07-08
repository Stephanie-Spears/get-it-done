from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
#8888 on mine, but sql says 8889
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:1alpha1@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#class extends db object (with a model class inside it) which we specified above
class Task(db.Model):
#data associated with id field of Task class will go into my db column, as an integer, and representing the primary key for this class and database associated with this tasks
    id = db.Column(db.Integer, primary_key=True)
    #column in database called name, using string of 120 max char
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

tasks = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)

    return render_template('todos.html',title="Get It Done!", tasks=tasks)


if __name__ == '__main__':
    app.run()
