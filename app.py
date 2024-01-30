from flask import Flask, redirect,render_template, request 
from flask_sqlalchemy import SQLAlchemy #install it my pip install flask-sqlalchemy
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str: #data you want to see is printed using repr
        return f"{self.sno}-{self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()  # query up all to do

    return render_template('index.html', alltodo=alltodo)
 
    #here we are passing alltodo to html page so we can use
    #to serve html pages which are saved in templates
    # return "Hello WOrld"

@app.route('/about') #path to different web pages
def about():
    return render_template('about.html')

@app.route('/update/<int:sno>', methods=['GET', 'POST']) #path to different web pages
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    

if __name__=="__main__":
    app.run(debug=True,port=8000) #debug means if error so show it on browser and to run on specific port use port