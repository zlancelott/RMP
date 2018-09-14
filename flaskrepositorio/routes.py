from flask import render_template, url_for, redirect, flash, request
from flaskrepositorio.forms import LoginForm
from flaskrepositorio import app, db, bcrypt
from flaskrepositorio.models import User, Subject
from flask_login import login_user, current_user, login_required, logout_user
from ftplib import FTP
from flaskrepositorio.funcs import download_ftp_files, remove_files
import urllib
import os


# Conexão FTP
ftp = FTP('192.168.15.5')
ftp.login(user='FTP_Server', passwd='ftpserver')


disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
               {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]


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


# Página que será aberta ao clicar em uma aula
@app.route("/disciplina/<string:disciplina>/aula")
def aula(disciplina):
    global disciplinas

    # Conexão FTP
    ftp = FTP('192.168.15.5')
    ftp.login(user='FTP_Server', passwd='ftpserver')

    # print("AULAAAAAAAAAAAAAAAAAAAAAAAAA")
    # print("Disciplina em Aula:", disciplina)

    # Acessando a pasta no servidor correspondente as aulas da disciplina
    path_lessons = "/Computer Science/7-semester/%s/" % (disciplina)
    ftp.cwd(path_lessons)
    lessons = ftp.nlst()  # Listando as aulas da disciplina

    aulas = []
    for j in range(len(lessons)):
        aulas.append({})
        aulas[j]["id"] = j
        aulas[j]["nome"] = lessons[j]

    # Acessando as imagens da aula
    path = "/Computer Science/7-semester/%s/Aula 01/" % (disciplina)
    ftp.cwd(path)

    imagens = ftp.nlst()

    # Download das imagens
    download_ftp_files()

    # Criando link para imagens da pasta static/cache
    nomes_arquivos = []
    arq = []
    for i in range(len(imagens)):
        nomes_arquivos.append(imagens[i])
        imagens[i] = url_for('static', filename="cache/" + imagens[i])
        arq.append({})
        arq[i]['nome'] = nomes_arquivos[i]
        arq[i]['endereco'] = imagens[i]

    print(arq)

    # # Removendo imagens da pasta cache
    # remove_files()

    #############################

    # disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
    #                {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]

    return render_template('galeria.html', title="Aula 01", arquivos=arq, nomes_arquivos=nomes_arquivos, disciplina=disciplina, disciplinas=disciplinas, aulas=aulas)


# Página que é aberta ao clicar em um arquivo
@app.route("/disciplina/<string:disciplina>/aula/<string:nome_imagem>")
def vizualizando_imagem(disciplina, nome_imagem):
    global disciplinas

    # Conexão FTP
    ftp = FTP('192.168.15.5')
    ftp.login(user='FTP_Server', passwd='ftpserver')

    # print("AULAAAAAAAAAAAAAAAAAAAAAAAAA")
    # print("Disciplina em Aula:", disciplina)

    # Acessando a pasta no servidor correspondente as aulas da disciplina
    path_lessons = "/Computer Science/7-semester/%s/" % (disciplina)
    ftp.cwd(path_lessons)
    lessons = ftp.nlst()  # Listando as aulas da disciplina

    aulas = []
    for j in range(len(lessons)):
        aulas.append({})
        aulas[j]["id"] = j
        aulas[j]["nome"] = lessons[j]

    print("Disciplina: ", disciplina)

    endereco_imagem = url_for('static', filename="Conteudo/computacao/7-semestre/%s/Aula 01/" % (disciplina) + nome_imagem)

    # disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
    #                {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]

    return render_template('vizualizando_imagem.html', disciplina=disciplina, disciplinas=disciplinas, imagem=endereco_imagem, nome_imagem=nome_imagem,
                           aulas=aulas)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return "ftp://FTP_Server:ftpserver@192.168.15.5/Computer%20Science/7-semester/Teoria%20da%20Computa%E7%E3o/Aula%2001/" + filename


# Página que será aberta ao clicar em uma disciplina
@app.route("/disciplina/<string:disciplina>")
def disciplina(disciplina):
    global disciplinas

    # Conexão FTP
    ftp = FTP('192.168.15.5')
    ftp.login(user='FTP_Server', passwd='ftpserver')

    # disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
    #                {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]

    # Acessando a pasta no servidor correspondente as aulas da disciplina
    path_lessons = "/Computer Science/7-semester/%s/" % (disciplina)
    ftp.cwd(path_lessons)
    lessons = ftp.nlst()  # Listando as aulas da disciplina

    aulas = []
    for j in range(len(lessons)):
        aulas.append({})
        aulas[j]["id"] = j
        aulas[j]["nome"] = lessons[j]

    return render_template('aulas.html', title=disciplina, aulas=aulas, disciplinas=disciplinas)


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    global disciplinas

    #disciplinas = list(current_user.disciplinas)
    # disciplinas = [{"id": "12", "nome": "Teoria da Computação"}, {"id": "13", "nome": "Gestão de Projetos"},
    #                {"id": "14", "nome": "Trabalho de Conclusão"}, {"id": "15", "nome": "Processamento Digital de Imagens"}]

    return render_template('home.html', disciplinas=disciplinas)
