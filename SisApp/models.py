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

    def __init__(self, nome, valor, condominio):
        self.nome = nome
        self.valor = valor
        self.condominios.append(condominio)



def alterar_condominio(id, nome):
    condominio = Condominio.query.get(id)

    if condominio is not None:
        condominio.nome = nome
        db.session.commit()
    else:
        raise Exception('Condominio não existe!')


def remover_condominio(id):
    condominio = Condominio.query.get(id)

    if condominio is not None:
        db.session.delete(condominio)
        db.session.commit()
    else:
        raise Exception('Condominio não existe!')

def alterar_apartamento(id, descricao):
    apartamento = Apartamento.query.get(id)

    if apartamento is not None:
        apartamento.descricao = descricao
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


def alterar_morador(id, nome):
    morador = Morador.query.get(id)

    if morador is not None:
        morador.nome = nome
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

def alterar_servico(id, nome, condominio = None):
    servico = Servico.query.get(id)

    if servico is not None:
        servico.nome = nome
        servico.condominios.append(condominio)
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
