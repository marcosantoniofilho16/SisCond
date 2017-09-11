from SisApp import db, models
import unittest

class SisAppTestCase(unittest.TestCase):
	def setUp(self):
		db.drop_all()
		db.create_all()

	def test_add_condominio(self):
		db.session.add(models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1'))
		db.session.add(models.Condominio('Cond2','Rua 2', 'Cidade2', 'Estado2', '2'))
		db.session.add(models.Condominio('Cond3','Rua 3', 'Cidade3', 'Estado3', '3'))
		db.session.add(models.Condominio('Cond4','Rua 4', 'Cidade4', 'Estado4', '4'))
		db.session.commit()

		condominios = models.Condominio.query.all()
		self.assertEqual(condominios[3].nome, 'Cond4')
		condominio = models.Condominio.query.filter_by(nome = 'Cond1').first()
		self.assertEqual(condominio.nome, 'Cond1')
		self.assertEqual(len(condominios), 4)

	def test_alterar_condominio(self):
		condominio = models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1')
		db.session.add(condominio)
		db.session.commit()
		models.alterar_condominio(condominio.id, 'CondX')
		self.assertEqual(condominio.nome, 'CondX')

	def test_remover_condominio(self):
		condominio = models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1')
		db.session.add(condominio)
		db.session.commit()
		count = len(models.Condominio.query.all())
		models.remover_condominio(condominio.id)
		self.assertNotEqual(len(models.Condominio.query.all()), count)
		self.assertEqual(len(models.Condominio.query.all()), count-1)
    	

	def test_add_apartamento(self):
		db.session.add(models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1'))
		db.session.add(models.Apartamento('Descrição1','Situação1', 1))
		db.session.add(models.Apartamento('Descrição2','Situação2', 1))
		db.session.add(models.Apartamento('Descrição3','Situação3', 1))
		db.session.add(models.Apartamento('Descrição4','Situação4', 1))
		db.session.commit()

		apartamentos = models.Apartamento.query.all()
		self.assertEqual(apartamentos[3].descricao, 'Descrição4')
		apartamento = models.Apartamento.query.filter_by(descricao = 'Descrição1').first()
		self.assertEqual(apartamento.descricao, 'Descrição1')
		self.assertEqual(len(apartamentos), 4)


	def test_alterar_apartamento(self):
		db.session.add(models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1'))
		apartamento = models.Apartamento('Descrição1','Situação1', 1)
		db.session.add(apartamento)
		db.session.commit()
		models.alterar_apartamento(apartamento.id, 'DescrX')
		self.assertEqual(apartamento.descricao, 'DescrX')

	def test_remover_apartamento(self):
		db.session.add(models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1'))
		apartamento = models.Apartamento('Descrição1','Situação1', 1)
		db.session.add(apartamento)
		db.session.commit()
		count = len(models.Apartamento.query.all())
		models.remover_apartamento(apartamento.id)
		self.assertNotEqual(len(models.Apartamento.query.all()), count)
		self.assertEqual(len(models.Apartamento.query.all()), count-1)


	def test_add_morador(self):
		db.session.add(models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1'))
		db.session.add(models.Apartamento('Descrição1','Situação1', 1))
		db.session.add(models.Apartamento('Descrição2','Situação2', 1))
		db.session.add(models.Apartamento('Descrição3','Situação3', 1))
		db.session.add(models.Apartamento('Descrição4','Situação4', 1))

		db.session.add(models.Morador('Nome1', 'Telefone1', 'CPF1', 1))
		db.session.add(models.Morador('Nome2', 'Telefone2', 'CPF2', 2))
		db.session.add(models.Morador('Nome3', 'Telefone3', 'CPF3', 3))
		db.session.add(models.Morador('Nome4', 'Telefone4', 'CPF4', 4))
		db.session.commit()

		moradores = models.Morador.query.all()
		self.assertEqual(moradores[3].nome, 'Nome4')
		morador = models.Morador.query.filter_by(nome = 'Nome1').first()
		self.assertEqual(morador.nome, 'Nome1')
		self.assertEqual(len(moradores), 4)

	def test_alterar_morador(self):
		db.session.add(models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1'))
		db.session.add(models.Apartamento('Descrição1','Situação1', 1))
		db.session.add(models.Apartamento('Descrição2','Situação2', 1))
		db.session.add(models.Apartamento('Descrição3','Situação3', 1))
		db.session.add(models.Apartamento('Descrição4','Situação4', 1))

		morador = models.Morador('Nome1', 'Telefone1', 'CPF1', 1)
		db.session.add(morador)
		db.session.commit()
		models.alterar_morador(morador.id, 'NomeX')
		self.assertEqual(morador.nome, 'NomeX')

	def test_remover_morador(self):
		db.session.add(models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1'))
		db.session.add(models.Apartamento('Descrição1','Situação1', 1))
		db.session.add(models.Apartamento('Descrição2','Situação2', 1))
		db.session.add(models.Apartamento('Descrição3','Situação3', 1))
		db.session.add(models.Apartamento('Descrição4','Situação4', 1))

		morador = models.Morador('Nome1', 'Telefone1', 'CPF1', 1)
		db.session.add(morador)
		db.session.commit()
		count = len(models.Morador.query.all())
		models.remover_morador(morador.id)
		self.assertNotEqual(len(models.Morador.query.all()), count)
		self.assertEqual(len(models.Morador.query.all()), count-1)


	def test_add_servico(self):
		condominio = models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1')
		condominio2 = models.Condominio('Cond2','Rua 2', 'Cidade2', 'Estado2', '2')
		db.session.add(condominio)
		db.session.add(condominio2)
		db.session.add(models.Servico('Serviço1', 100, condominio))
		db.session.add(models.Servico('Serviço2', 200, condominio))
		db.session.add(models.Servico('Serviço3', 300, condominio2))
		db.session.add(models.Servico('Serviço4', 400, condominio2))
		db.session.commit()

		
		servicos = models.Servico.query.all()
		self.assertEqual(servicos[3].nome, 'Serviço4')
		self.assertEqual(servicos[3].condominios[0].nome, 'Cond2')
		servico = models.Servico.query.filter_by(nome = 'Serviço1').first()
		self.assertEqual(servico.nome, 'Serviço1')
		self.assertEqual(len(servicos), 4)

	def test_alterar_servico(self):
		condominio = models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1')
		condominio2 = models.Condominio('Cond2','Rua 2', 'Cidade2', 'Estado2', '2')
		db.session.add(condominio)
		db.session.add(condominio2)

		servico = models.Servico('Serviço1', 100, condominio)
		db.session.add(servico)
		db.session.commit()
		models.alterar_servico(servico.id, 'ServX', condominio2)
		self.assertEqual(servico.nome, 'ServX')


	def test_remover_servico(self):
		condominio = models.Condominio('Cond1','Rua 1', 'Cidade1', 'Estado1', '1')
		condominio2 = models.Condominio('Cond2','Rua 2', 'Cidade2', 'Estado2', '2')
		db.session.add(condominio)
		db.session.add(condominio2)

		servico = models.Servico('Serviço1', 100, condominio)
		db.session.add(servico)
		db.session.commit()

		count = len(models.Servico.query.all())
		models.remover_servico(servico.id)
		self.assertNotEqual(len(models.Servico.query.all()), count)
		self.assertEqual(len(models.Servico.query.all()), count-1)



if __name__ == '__main__':
	unittest.main()
