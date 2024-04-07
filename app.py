from flask import Flask, render_template, request, redirect
from database import db
from models import Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)


def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/')
def index():
    try:
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        return render_template('error.html', error=str(e))
        

@app.route('/add', methods=['POST'])
def add_task():
    try:
        content = request.form['content']
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/complete/<int:id>')
def complete_task(id):
    try:
        task = Task.query.get_or_404(id)
        task.completed = True
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/delete/<int:id>')
def delete_task(id):
    try:
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
