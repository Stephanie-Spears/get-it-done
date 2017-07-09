from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
#8888 on mine, but sql says 8889
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:1alpha1@localhost:8889/get-it-done'
#echo SQLAlchemy messages in a verbose way when we use python in terminal to run these scripts
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#class extends db object (with class "model" inside it) which we specified above. Model allows us to do stuff like queryAll
class Task(db.Model):
#any time we modify the Model class with a new column, we will have to use drop_all() and then create_all() in order for those changes to be viewed in the database itself (losing anything in the db). Theres also Flask-Migrate, which doesn't make you lose all your data (but we haven't learned it yet)
#data associated with id field of Task class will go into my db column, as an integer, and representing the primary key for this class and database associated with this tasks
    id = db.Column(db.Integer, primary_key=True)
    #column in database called name, using string of 120 max char
    name = db.Column(db.String(120))

#new property for our task class, of Boolean type--you can specify a default value with ,default=False
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

#pulls all Task objects from the database(even the "deleted" ones which have been set to False. We can fix it so deleted wont show by adding a filter to the query)
    # tasks = Task.query.all()
    tasks = Task.query.filter_by(completed=False).all()
#give completed tasks it's own section to be displayed on, and remember to pass it into the render_template just like we did with tasks=tasks--and then actually DO something with it in the template by updating the html
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


#old delete-task handler below:
# @app.route('/delete-task', methods=['POST'])
# def delete_task():
#
# #we have to convert the task_id parameter into an int because it tries to send it as a string
#     task_id = int(request.form['task-id'])
#     #passing task_id to get so we can get the specific task from the database
#     task = Task.query.get(task_id)
#     #asking the database to delete that specific task, and then commit it (which is what actually runs the queries to the database to be completed)
#     db.session.delete(task)
#     db.session.commit()
#
# #not returning content from this request, so we are redirecting them to the main page after the query finishes
#     return redirect('/')


if __name__ == '__main__':
    app.run()
