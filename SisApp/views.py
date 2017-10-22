from SisApp import app, db, models
from flask import render_template, redirect, url_for, request, session, flash

app.secret_key = 'senha'
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'usuario' in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		usuario = request.form['usuario']
		senha = request.form['senha']
		u = models.Usuario.query.filter_by(login = usuario).first()

		if(u is not None and u.senha == senha):
			session['usuario'] = u.tipo
			flash('Login efetuado com sucesso!')
			return redirect(url_for('homepage'))
		else:
			flash('Tentativa de Login falhou!')
			return render_template('login.html')
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('usuario')
	flash('Logout efetuado com sucesso!')
	return redirect(url_for('homepage'))


@app.route('/')
@app.route('/home')
def homepage():
	return render_template('index.html')

@app.route('/condominio', methods=['GET', 'POST'])
def Condominio():
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		nome = request.form['nome']
		endereco = request.form['endereco']
		cidade = request.form['cidade']
		estado = request.form['estado']
		cnpj = request.form['cnpj']
		db.session.add(models.Condominio(nome, endereco, cidade, estado, cnpj))
		db.session.commit()
		flash('Cadastro realizado com sucesso!')
	return render_template('condominio.html', Listagem = models.Condominio.query.all(), servicos = models.Servico.query.all(), Alterar = 'alterarCondominio', Excluir = 'removerCondominio')


@app.route('/condominio/excluir/<int:index>')
def removerCondominio(index):
	if 'usuario' not in  session:
		return redirect(url_for('homepage'))
	models.remover_condominio(index)
	flash('Registro excluido com sucesso!')
	return redirect(url_for('Condominio'))

@app.route('/condominio/alterar/<int:index>', methods=['GET', 'POST'])
def alterarCondominio(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		nome = request.form['nome']
		endereco = request.form['endereco']
		cidade = request.form['cidade']
		estado = request.form['estado']
		cnpj = request.form['cnpj']
		models.alterar_condominio(index, nome, endereco, cidade, estado, cnpj)
		flash('Registro alterado com sucesso!')
		return redirect(url_for('Condominio'))
	condominio = models.Condominio.query.get(index)
	return render_template('condominio.html', Informacoes = condominio, index = index, Listagem = models.Condominio.query.all(), servicos = models.Servico.query.all(), Alterar = 'alterarCondominio', Excluir = 'removerCondominio')

@app.route('/apartamento', methods=['GET', 'POST'])
def Apartamento():
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		descricao = request.form['descricao']
		situacao = request.form['situacao']
		condominio = request.form['condominio']
		db.session.add(models.Apartamento(descricao, situacao, condominio))
		db.session.commit()
		flash('Cadastro realizado com sucesso!')
	return render_template('apartamento.html', condominios = models.Condominio.query.all(), Listagem = models.Apartamento.query.all(), Alterar = 'alterarApartamento', Excluir = 'removerApartamento')

@app.route('/apartamento/excluir/<int:index>')
def removerApartamento(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	models.remover_apartamento(index)
	flash('Registro excluido com sucesso!')
	return redirect(url_for('Apartamento'))

@app.route('/apartamento/alterar/<int:index>', methods=['GET', 'POST'])
def alterarApartamento(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		descricao = request.form['descricao']
		situacao = request.form['situacao']
		condominio = request.form['condominio']
		models.alterar_apartamento(index, descricao, situacao, condominio)
		flash('Registro alterado com sucesso!')
		return redirect(url_for('Apartamento'))
	apartamento = models.Apartamento.query.get(index)
	return render_template('apartamento.html', Informacoes = apartamento, index = index, condominios = models.Condominio.query.all(), Listagem = models.Apartamento.query.all(), Alterar = 'alterarApartamento', Excluir = 'removerApartamento')


@app.route('/morador', methods=['GET', 'POST'])
def Morador():
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		nome = request.form['nome']
		telefone = request.form['telefone']
		cpf = request.form['cpf']
		apartamento = request.form['apartamento']
		db.session.add(models.Morador(nome, telefone, cpf, apartamento))
		db.session.commit()
		flash('Cadastro realizado com sucesso!')
	return render_template('morador.html', apartamentos = models.Apartamento.query.all(), Listagem = models.Morador.query.all(), Alterar = 'alterarMorador', Excluir = 'removerMorador')

@app.route('/morador/excluir/<int:index>')
def removerMorador(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	models.remover_morador(index)
	flash('Registro excluido com sucesso!')
	return redirect(url_for('Morador'))

@app.route('/morador/alterar/<int:index>', methods=['GET', 'POST'])
def alterarMorador(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		nome = request.form['nome']
		telefone = request.form['telefone']
		cpf = request.form['cpf']
		apartamento = request.form['apartamento']
		models.alterar_morador(index, nome, telefone, cpf, apartamento)
		flash('Registro alterado com sucesso!')
		return redirect(url_for('Morador'))
	morador = models.Morador.query.get(index)
	return render_template('morador.html', Informacoes = morador, index = index, apartamentos = models.Apartamento.query.all(), Listagem = models.Morador.query.all(), Alterar = 'alterarMorador', Excluir = 'removerMorador')

@app.route('/servico', methods=['GET', 'POST'])
def Servico():
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		nome = request.form['nome']
		valor = request.form['valor']
		db.session.add(models.Servico(nome, valor))
		db.session.commit()
		flash('Cadastro realizado com sucesso!')
	return render_template('servico.html', Listagem = models.Servico.query.all(), Alterar = 'alterarServico', Excluir = 'removerServico')

@app.route('/servico/excluir/<int:index>')
def removerServico(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	models.remover_servico(index)
	flash('Registro excluido com sucesso!')
	return redirect(url_for('Servico'))

@app.route('/servico/alterar/<int:index>', methods=['GET', 'POST'])
def alterarServico(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		nome = request.form['nome']
		valor = request.form['valor']
		models.alterar_servico(index, nome, None, valor)
		flash('Registro alterado com sucesso!')
		return redirect(url_for('Servico'))
	servico = models.Servico.query.get(index)
	return render_template('servico.html', Informacoes = servico, index = index, Listagem = models.Servico.query.all(), Alterar = 'alterarServico', Excluir = 'removerServico')

@app.route('/prestacao', methods=['GET', 'POST'])
def PrestacaoServico():
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		id_condominio = request.form['condominio']
		id_servico = request.form['servico']
		db.session.add(models.CondominioServico(id_condominio, id_servico))
		db.session.commit()
		flash('Cadastro realizado com sucesso!')
	return render_template('condominioServico.html', Listagem = models.CondominioServico.query.all(), condominios = models.Condominio.query.all(), servicos = models.Servico.query.all(), Alterar = 'alterarPrestacaoServico', Excluir = 'removerPrestacaoServico')

@app.route('/prestacao/excluir/<int:index>')
def removerPrestacaoServico(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	models.remover_condominio_servico(index)
	flash('Registro excluido com sucesso!')
	return redirect(url_for('PrestacaoServico'))

@app.route('/prestacao/alterar/<int:index>', methods=['GET', 'POST'])
def alterarPrestacaoServico(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		id_condominio = request.form['condominio']
		id_servico = request.form['servico']
		models.alterar_condominio_servico(index, id_condominio, id_servico)
		flash('Registro alterado com sucesso!')
		return redirect(url_for('PrestacaoServico'))
	condominio_servico = models.CondominioServico.query.get(index)
	return render_template('condominioServico.html', Informacoes = condominio_servico, index = index, Listagem = models.CondominioServico.query.all(), condominios = models.Condominio.query.all(), servicos = models.Servico.query.all(), Alterar = 'alterarPrestacaoServico', Excluir = 'removerPrestacaoServico')

@app.route('/ajuda', methods=['GET', 'POST'])
def Ajuda():
	if request.method == 'POST':
		email = request.form['email']
		tipo = request.form['tipo']
		msg = request.form['msg']
		db.session.add(models.Contato(email, tipo, msg))
		db.session.commit()
		flash('Cadastro realizado com sucesso!')
	return render_template('ajuda.html', Listagem = models.Contato.query.all())


@app.route('/contato/excluir/<int:index>')
def removerContato(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	models.remover_contato(index)
	flash('Registro excluido com sucesso!')
	return redirect(url_for('Ajuda'))


@app.route('/usuario', methods=['GET', 'POST'])
def Usuario():
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		login = request.form['login']
		senha = request.form['senha']
		tipo = request.form['tipo']
		db.session.add(models.Usuario(login, senha, tipo))
		db.session.commit()
		flash('Cadastro realizado com sucesso!')
	return render_template('usuario.html', Listagem = models.Usuario.query.all(), Alterar = 'alterarUsuario', Excluir = 'removerUsuario')


@app.route('/usuario/excluir/<int:index>')
def removerUsuario(index):
	if 'usuario' not in  session:
		return redirect(url_for('homepage'))
	models.remover_usuario(index)
	flash('Registro excluido com sucesso!')
	return redirect(url_for('Usuario'))

@app.route('/usuario/alterar/<int:index>', methods=['GET', 'POST'])
def alterarUsuario(index):
	if 'usuario' not in session:
		return redirect(url_for('homepage'))
	if request.method == 'POST':
		login = request.form['login']
		senha = request.form['senha']
		tipo = request.form['tipo']
		models.alterar_usuario(index, login, senha, tipo)
		flash('Registro alterado com sucesso!')
		return redirect(url_for('Usuario'))
	usuario = models.Usuario.query.get(index)
	return render_template('usuario.html', Informacoes = usuario, index = index, Listagem = models.Usuario.query.all(), Alterar = 'alterarUsuario', Excluir = 'removerUsuario')

