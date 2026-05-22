from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
todos=[]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db=SQLAlchemy(app)

class Todos(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)

    created_at=db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    completed=db.Column(
        db.Boolean,
        default=False
    )
with app.app_context():
    db.create_all()


@app.route('/complete/<int:id>')
def complete(id):
    todo=Todos.query.get_or_404(id)
    todo.completed=not todo.completed
    db.session.commit()
    return redirect("/")
@app.route('/')
def index():
    todos=Todos.query.all()
    return render_template('index.html',todos=todos)

@app.route('/add',methods=['POST'])
def add():
    todo = request.form.get("todo")
    new_todo = Todos(content=todo)
    if todo:
        db.session.add(new_todo)
        db.session.commit()
        return redirect("/")
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todos.query.get_or_404(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")

if __name__=='__main__':
    app.run(debug=True)