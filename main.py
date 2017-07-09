from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
#installed Flask_Migrate onto flask-env, can be accessed with:
#from flask_migrate import Migrate
#migrate = Migrate(app, db)
#Now I can create a migration repository with "flask db init" in terminal. Adds a migation folder to terminal. After that, can generate initial migration with "flask db migrate". Finally, you can apply the migration to the database with "flask db upgrade". Then each time the database models change, repeat the migrate and upgrade commands. To sync the db in another system just refresh migrations folder from source control and run the upgrade command. to see all commands, "flask db --help"

app = Flask(__name__)
app.config['DEBUG'] = True
#8888 on mine, but sql says 8889
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:1alpha1@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)


@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()
