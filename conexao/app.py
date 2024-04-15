from flask import Flask,render_template,request,flash,redirect,url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cashflow'
app.config['SECRET_KEY'] = 'chave'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(50))

class Receitas(db.Model):
    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date)
    valor = db.Column(db.Integer)
    descricao = db.Column(db.String(150))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Despesas(db.Model):
    id_despesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date)
    valor = db.Column(db.Integer)
    descricao = db.Column(db.String(150))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

@app.route('/')
def entrar():
    return render_template('Entrar.html')

@app.route('/geral')
def geral():
    if 'id' in session:
        return render_template('Geral.html')
    else:
        return redirect(url_for('login_form'))

@app.route('/listagem')
def listagem():
    # Crie as seleções SQL para cada consulta
    selecao_despesas = Despesas.query.filter_by(id_usuario=session['id']).all()
    selecao_receitas = Receitas.query.filter_by(id_usuario=session['id']).all()
    dados = []

    for receita in selecao_receitas:
        dados.append(receita)

    for despesa in selecao_despesas:
        dados.append(despesa)

    return render_template('Listagem.html', despesas=selecao_despesas, receitas=selecao_receitas, tudo=dados)

@app.route('/config')
def config():
    return render_template('Config.html')

@app.route('/login')
def login_form():
	return render_template('Login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')

    user = Usuario.query.filter_by(email=email).first()

    if user and senha == user.senha:
        session['id'] = user.id
        if 'next' in session:
            next_route = session.pop('next')
            return redirect(url_for(next_route))
        return redirect(url_for('geral'))
    else:
        flash(f'Nome ou senha incorretos', 'error')
        return redirect(url_for('login_form'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id', None)
    return redirect(url_for('login_form'))

@app.route('/novo_user')
def novo_user():
    return render_template('Cadastro.html', titulo='Novo Usuário')

@app.route('/criar_user', methods=['POST'])
def criar_user():
    email = request.form['email']
    senha = request.form['senha']
    nome = request.form['nome']

    user = Usuario.query.filter_by(email=email).first()
    if user:
        flash('Usuário já existe', 'error')
        return redirect(url_for('novo_user'))
    else:
        #senha_hash = generate_password_hash(senha).decode('utf-8')
        novo_usuario = Usuario(email=email, senha=senha, nome=nome)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso', 'success')
        return redirect(url_for('novo_user'))
@app.route('/cadastrolista')
def cadastrolista():
    return render_template('CadastroListagem.html')

@app.route('/cadastro_despesa', methods=['POST'])
def cadastro_despesa():
    data = request.form['data']
    valor = request.form['valor']
    descricao = request.form['descricao']
    categoria = request.form['categoria']
    if categoria== 'Despesa':
        despesa = Despesas.query.filter_by(descricao=descricao).first()
        nova_despesa = Despesas(data=data, valor=valor, descricao=descricao, id_usuario=session['id'])
        db.session.add(nova_despesa)
        db.session.commit()
        flash('Usuário cadastrado com sucesso', 'success')
        return redirect(url_for('cadastrolista'))
    else:
        receita = Receitas.query.filter_by(descricao=descricao).first()
        nova_receita = Receitas(data=data, valor=valor, descricao=descricao, id_usuario=session['id'])
        db.session.add(nova_receita)
        db.session.commit()
        flash('Usuário cadastrado com sucesso', 'success')
        return redirect(url_for('cadastrolista'))

if __name__ == '__main__':
    app.run(debug=True)