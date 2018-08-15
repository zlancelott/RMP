from flask import render_template, url_for, redirect, flash, request
from flaskrepositorio.forms import LoginForm
from flaskrepositorio import app, db, bcrypt
from flaskrepositorio.models import User, Disciplina
from flask_login import login_user, current_user, login_required, logout_user


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(matricula=form.matricula.data).first()

        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your email and password', 'danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/disciplina/<int:disciplina_id>")
def disciplina(disciplina_id):
    disciplina = Disciplina.query.get_or_404(disciplina_id)
    return render_template('disciplina.html', title=disciplina.nome, disciplina=disciplina)


@app.route("/home")
@login_required
def home():
    disciplinas = list(current_user.disciplinas)

    return render_template('home.html', disciplinas=disciplinas)
