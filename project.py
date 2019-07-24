from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Derya/Desktop/app-flask/project.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    todos = Projects.query.all()
    return render_template("index.html",todos=todos)

@app.route("/add",methods=["POST"])
def addToDo():
    title =request.form.get("title")
    newtodo =Projects(title =title,complete =False)
    db.session.add(newtodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo =Projects.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<string:id>")
def update(id):
    todo=Projects.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))      

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(80))
    complete =db.Column(db.Boolean)


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)