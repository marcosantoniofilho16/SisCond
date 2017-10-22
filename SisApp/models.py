from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from SisApp import db


condominioServicos = db.Table(

    'condominioServicos',

    db.Column('id_condominio',
            db.Integer,
            db.ForeignKey('condominio.id')),

    db.Column('id_servico',
            db.Integer,
            db.ForeignKey('servico.id'))
 )


class Condominio (db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True)

    nome = db.Column(db.String(80))
    endereco = db.Column(db.String(80))
    cidade = db.Column(db.String(80))
    estado = db.Column(db.String(10))
    cnpj = db.Column(db.String(20))

    apartamentos = db.relationship(              # Para os relacionamento de 1 : N
        'Apartamento',
        backref='condominio',
        lazy='dynamic')

    servicos = db.relationship(                 # Para os relacionamento de N : N

        'Servico',

        secondary=condominioServicos,

        backref=db.backref(
            'condominio',
            lazy='dynamic'))

    def __init__(self, nome, endereco, cidade, estado, cnpj):
        self.nome = nome
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cnpj = cnpj

    def __repr__(self):
        return '{}'.format(self.nome)

class Apartamento (db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True)

    descricao = db.Column(db.String(80))
    situacao = db.Column(db.String(80))

    id_condominio = db.Column(                    # Para os relacionamento de 1 : N
        db.Integer,
        db.ForeignKey('condominio.id'))

    def __init__(self, descricao, situacao, id_condominio):
        self.descricao = descricao
        self.situacao = situacao
        self.id_condominio = id_condominio

    def __repr__(self):
        return '{}'.format(self.descricao)


class Morador (db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True)

    nome = db.Column(db.String(80))
    telefone = db.Column(db.String(80))
    cpf = db.Column(db.String(80))

    id_apartamento = db.Column(
        db.Integer,
        db.ForeignKey('apartamento.id'))

    apartamento = db.relationship(             # Para os relacionamento de 1 : 1
            'Apartamento',
            backref='morador',
            uselist=False)

    def __init__(self, nome, telefone, cpf, id_apartamento):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.id_apartamento = id_apartamento

    def __repr__(self):
        return '{}'.format(self.nome)


class Servico (db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True)

    nome = db.Column(db.String(80))
    valor = db.Column(db.Float)

    condominios = db.relationship(          # Para os relacionamento de N : N
        'Condominio',
        secondary=condominioServicos,
        backref=db.backref(
        'servico',
        lazy='dynamic'))

    def __init__(self, nome, valor, condominio = None):
        self.nome = nome
        self.valor = valor
        if (condominio != None):
            self.condominios.append(condominio)

    def __repr__(self):
        return '{}'.format(self.nome)

class CondominioServico (db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True)

    id_condominio = db.Column(db.Integer)
    id_servico = db.Column(db.Integer)

    def __init__(self, id_condominio, id_servico):
        self.id_condominio = id_condominio
        self.id_servico = id_servico

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(40))
    tipo = db.Column(db.String(40))
    msg = db.Column(db.String(250))

    def __init__(self, email, tipo, msg):
        self.email = email
        self.tipo = tipo
        self.msg = msg

    def __repr__(self):
        return '{}'.format(self.nome)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(40))
    senha = db.Column(db.String(20))
    tipo = db.Column(db.String(1))

    def __init__(self, login, senha, tipo):
        self.login = login
        self.senha = senha
        self.tipo = tipo

    def __repr__(self):
        return '{}'.format(self.login)



def alterar_condominio(id, nome, endereco = None, cidade = None, estado = None, cnpj = None):
    condominio = Condominio.query.get(id)

    if condominio is not None:
        condominio.nome = nome
        if endereco is not None:
            condominio.endereco = endereco
            condominio.cidade = cidade
            condominio.estado = estado
            condominio.cnpj = cnpj
        db.session.commit()
    else:
        raise Exception('Condominio não existe!')


def remover_condominio(id):
    condominio = Condominio.query.get(id)

    if condominio is not None:
        condominio.servicos.clear()
        db.session.commit()
        db.session.delete(condominio)
        db.session.commit()
    else:
        raise Exception('Condominio não existe!')

def alterar_apartamento(id, descricao, situacao = None, condominio = None):
    apartamento = Apartamento.query.get(id)

    if apartamento is not None:
        apartamento.descricao = descricao
        if situacao is not None:
            apartamento.situacao = situacao
            apartamento.id_condominio = condominio
        db.session.commit()
    else:
        raise Exception('Apartamento não existe!')


def remover_apartamento(id):
    apartamento = Apartamento.query.get(id)

    if apartamento is not None:
        db.session.delete(apartamento)
        db.session.commit()
    else:
        raise Exception('Aparmento não existe!')


def alterar_morador(id, nome, telefone = None, cpf = None, apartamento = None):
    morador = Morador.query.get(id)

    if morador is not None:
        morador.nome = nome
        if telefone is not None:
            morador.telefone = telefone
            morador.cpf = cpf
            morador.id_apartamento = apartamento
        db.session.commit()
    else:
        raise Exception('Morador não existe!')


def remover_morador(id):
    morador = Morador.query.get(id)

    if morador is not None:
        db.session.delete(morador)
        db.session.commit()
    else:
        raise Exception('Morador não existe!')

def alterar_servico(id, nome, condominio = None, valor = None):
    servico = Servico.query.get(id)

    if servico is not None:
        servico.nome = nome
        if condominio is not None:
            servico.condominios.append(condominio)
        if valor is not None:
            servico.valor = valor
        db.session.commit()
    else:
        raise Exception('Serviço não existe!')


def remover_servico(id):
    servico = Servico.query.get(id)

    if servico is not None:
        servico.condominios.clear()
        db.session.commit()
        db.session.delete(servico)
        db.session.commit()
    else:
        raise Exception('Serviço não existe!')

def alterar_condominio_servico(id, condominio, servico):
    condominio_servico = CondominioServico.query.get(id)

    if condominio_servico is not None:
        condominio_servico.id_condominio = condominio
        condominio_servico.id_servico = servico
        db.session.commit()
    else:
        raise Exception('Prestação de Serviços não existe!')


def remover_condominio_servico(id):
    condominio_servico = CondominioServico.query.get(id)

    if condominio_servico is not None:
        db.session.delete(condominio_servico)
        db.session.commit()
    else:
        raise Exception('Prestação de Serviços não existe!')


def remover_contato(id):
    contato = Contato.query.get(id)

    if contato is not None:
        db.session.delete(contato)
        db.session.commit()
    else:
        raise Exception('Contato não existe!')


def alterar_usuario(id, login, senha, tipo):
    usuario = Usuario.query.get(id)

    if usuario is not None:
        usuario.login = login
        usuario.senha = senha
        usuario.tipo = tipo
        db.session.commit()
    else:
        raise Exception('Usuario não existe!')


def remover_usuario(id):
    usuario = Usuario.query.get(id)

    if usuario is not None:
        db.session.delete(usuario)
        db.session.commit()
    else:
        raise Exception('Usuario não existe!')
