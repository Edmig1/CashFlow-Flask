from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cashflow'
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

@app.route('/')
def entrar():
    return render_template('Entrar.html')

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

@app.route('/cadastro')
def cadastro():
    return render_template('CadastroListagem.html')

if __name__ == '__main__':
    app.run(debug=True)
