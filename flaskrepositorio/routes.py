from flask import render_template, url_for, redirect, flash, request
from flaskrepositorio.forms import LoginForm
from flaskrepositorio import app, db, bcrypt
from flaskrepositorio.models import User, Subject
from flask_login import login_user, current_user, login_required, logout_user
import os


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.matricula.data).first()

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


@app.route("/disciplina/<string:disciplina>/aula")
def aula(disciplina):
    path = "/Users/Lancelot/Documents/RMD/flaskrepositorio/static/Conteudo/computacao/7-semestre/%s/Aula 01/" %(disciplina)
    print(disciplina, "lalal")
    arquivos = os.listdir(path)


    for i in range(len(arquivos)):
        arquivos[i] = url_for('static', filename= "Conteudo/computacao/7-semestre/%s/Aula 01/"%(disciplina) + arquivos[i])

    print (arquivos)

    disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
                   {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]


    return render_template('arquivos.html', title="Aula 01", arquivos = arquivos, disciplinas=disciplinas)


@app.route("/disciplina/<string:disciplina>")
def disciplina(disciplina):

    aulas = os.listdir('/Users/Lancelot/Documents/RMD/flaskrepositorio/static/Conteudo/computacao/7-semestre/%s' % (disciplina))

    print(aulas)

    return render_template('disciplina.html', title=disciplina, aulas=aulas)


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    #disciplinas = list(current_user.disciplinas)
    disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
                   {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]

    return render_template('home.html', disciplinas=disciplinas)
