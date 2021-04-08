from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Path to DB: (relative path - create a db.sqlite file in directory)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create our DB:
db = SQLAlchemy(app)


# Class for to-do with all the entries in our db:
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique key for each managed by sqlalchemy
    title = db.Column(db.String(100))  # max 100 char here
    completed = db.Column(db.Boolean)  # t/f


@app.route('/')
def index():
    # show all todos - list of all items:
    todo_list = Todo.query.all()  # fetches all the data from db
    # print(todo_list)  # print items from db <obj and key no.>
    # now showing the items to the frontend, todo_list goes a params to base file:
    return render_template("base.html", todo_list=todo_list)


# this route works internally and does not show up:
# POST: since we are giving the data for insertion first time.
@app.route('/add', methods=["POST"])
def add():
    # adding new to-do:
    title = request.form.get("title")
    new_todo = Todo(title=title, completed=False)
    db.session.add(new_todo)  # add to db
    db.session.commit()  # commit db
    # now refresh/redirects page home to see changes:
    return redirect(url_for("index"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()  # commit db
    # now refresh/redirects page home to see changes:
    return redirect(url_for("index"))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()  # commit db
    # now refresh/redirects page home to see changes:
    return redirect(url_for("index"))


if __name__ == '__main__':
    # creates a db file:
    db.create_all()
    # create a new item to db:
    '''new_todo = Todo(title="todo 1", completed=False)
    db.session.add(new_todo)
    db.session.commit()'''

    app.run(debug=True)
