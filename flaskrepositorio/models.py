from flaskrepositorio import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


disciplina_identifier = db.Table('disciplina_identifier',
                                 db.Column('usuarios_id', db.Integer, db.ForeignKey('usuarios.id')),
                                 db.Column('disciplinas_id', db.Integer, db.ForeignKey('disciplinas.id'))
                                 )


class User(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.matricula}', '{self.password}')"


class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuarios = db.relationship("User",
                               secondary=disciplina_identifier,
                               backref=db.backref('disciplinas', lazy='dynamic'))

    def __repr__(self):
        return f"Disciplina('{self.nome}')"
