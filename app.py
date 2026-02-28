#imports 
from datetime import datetime
from flask import Flask , render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

#myapp 
app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db=SQLAlchemy(app)

# data class row of data
class myTask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(100),nullable=False)
    completed = db.Column(db.Integer,default=0)
    created = db.Column(db.DateTime,default=datetime.utcnow) 
    def __repr__(self):
        return f"Task {self.id}"


#routes to webpages
#HOME page
@app.route("/",methods=["POST","GET"])
def index():
    # add a task
    if request.method=="POST":
        current_task = request.form['content']
        new_task=myTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    #see all current task
    else:
        tasks=myTask.query.order_by(myTask.created).all()
        return render_template("index.html",tasks=tasks)

#deleteanitem
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
#editanitem
@app.route("/update/<int:id>",methods=["POST","GET"])
def update(id:int):
    task=myTask.query.get_or_404(id)
    if request.method=="POST":
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template("edit.html",task=task)
    
if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)