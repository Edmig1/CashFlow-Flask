from flask import Flask,render_template,request,flash,redirect,url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
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
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(50))

@app.route('/')
def entrar():
    if 'id' in session:
        return render_template('Geral.html')
    else:
        return redirect(url_for('login_form'))


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
        return redirect(url_for('entrar'))
    else:
        flash(f'Nome ou senha incorretos {email}  {senha} ', 'error')
        return redirect(url_for('login_form'))


#@app.route('/logout', methods=['POST'])
#def logout():
#    session.pop('id', None)
#    return redirect(url_for('index'))

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
        nova_despesa = Despesas(data=data, valor=valor, descricao=descricao)
        db.session.add(nova_despesa)
        db.session.commit()
        flash('Usuário cadastrado com sucesso', 'success')
        return redirect(url_for('cadastrolista'))
    else:
        receita = Receitas.query.filter_by(descricao=descricao).first()
        nova_receita = Receitas(data=data, valor=valor, descricao=descricao)
        db.session.add(nova_receita)
        db.session.commit()
        flash('Usuário cadastrado com sucesso', 'success')
        return redirect(url_for('cadastrolista'))

if __name__ == '__main__':
    app.run(debug=True)