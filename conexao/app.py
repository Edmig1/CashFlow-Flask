from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cashflow'
app.config['SECRET_KEY'] = 'chave'
db = SQLAlchemy(app)

class Receitas(db.Model):
    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date)
    valor = db.Column(db.Integer)
    descricao = db.Column(db.String(150))

class Despesas(db.Model):
    id_despesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date)
    valor = db.Column(db.Integer)
    descricao = db.Column(db.String(150))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome= db.Column(db.String(50))
    email= db.Column(db.String(100))
    senha= db.Column(db.String(50))

@app.route('/')
def entrar():
    return render_template('Entrar.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/geral')
def geral():
    return render_template('Geral.html')

@app.route('/listagem')
def listagem():

    ListaDespesas = Despesas.query.all()
    ListaReceitas = Receitas.query.all()

    return render_template('Listagem.html', despesas=ListaDespesas, receitas=ListaReceitas)

@app.route('/config')
def config():
    return render_template('Config.html')

@app.route('/cadastrolista')
def cadastrolista():
    return render_template('CadastroListagem.html')

@app.route('/cadastro')
def cadastro():
    return render_template('Cadastro.html')
@app.route('/criar_user', methods=['POST'])
def criar_user():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    user = Usuario.query.filter_by(email=email).first()
    senha_hash = generate_password_hash(senha).decode('utf-8')
    novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()
    flash('Usuário cadastrado com sucesso', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
