from flask import Flask
from flask import g, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, current_user, login_user, logout_user
import datetime
from models import User, Tasks, initialize_database
from forms import LoginForm, RegistrationForm, TaskForm

app = Flask("TaskList")
app.secret_key = 'super secret key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@app.route('/', methods=['GET'])
def index():
    today = datetime.datetime.today()

    return render_template("index.html", tasks=Tasks, today=today)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('in login')
    if request.method == 'POST':
        registered_user = User.filter(User.nikname == form.nikname.data).first()
        print('in if')
        if registered_user is None:
            flash('This Nikname is not exist')
            return redirect(url_for("login"))
        if registered_user.password != form.password.data:
            flash('Password is wrong')
            return redirect(url_for("login"))
        login_user(registered_user)
        flash('Login completed successfully')
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('registration.html', form = form)

    if request.method == 'POST':
        registered_user = User.filter(User.nikname == form.nikname.data).first()
        if registered_user is not None:
            flash('Nikname was used')
            return redirect(url_for("registration"))
        if form.nikname.data != "" :
            if form.password.data == form.confirm.data:
                User.create(nikname = form.nikname.data, firstname=form.firstname.data, lastname=form.lastname.data, password=form.password.data)
                flash('Registration completed successfully')
                return redirect(url_for("index"))
            else:
                flash('Passwords must match')
                return redirect(url_for("registration"))
        else:
            flash('Incorect nikname')
            return redirect(url_for("registration"))
    return render_template("registration.html", form=form)

@app.route('/create', methods=["GET", "POST"])
def create():
    form = TaskForm(user_id = g.user.id)
    if request.method == "POST":
        Tasks.create(user = form.user_id.data, task_title=form.title.data, task_text=form.task.data, task_date=form.date.data, task_to_date=form.date_to.data, task_status = form.status.data)
        flash('Task created successfully')
        return redirect(url_for("index"))
    return render_template("create.html",form=form)


@app.route('/delete/task/<int:task_id>', methods=["GET"])
def delete(task_id):
    delete = Tasks.delete().where(Tasks.id == task_id)
    delete.execute()
    flash('Task was deleted')
    return redirect(url_for("index"))


@app.route('/edit/task/<int:task_id>', methods=["GET", "POST"])
def edit(task_id):
    form = TaskForm(user_id = g.user.id)
    if request.method == "POST":
        q = Tasks.update(user = form.user_id.data, task_title=form.title.data, task_text=form.task.data, task_date=form.date.data, task_to_date=form.date_to.data, task_status = form.status.data).where(Tasks.id == task_id)
        q.execute()
        flash('Task edited successfully')
        return redirect(url_for("index"))
    task = Tasks.get(Tasks.id == task_id)
    form.user_id.data = task.user_id
    form.title.data = task.task_title
    form.task.data = task.task_text
    form.date.data = timestamp=task.task_date
    form.date_to.data = timestamp=task.task_to_date
    form.status.data = task.task_status
    return render_template("edit.html",form=form,task_id=task_id)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)