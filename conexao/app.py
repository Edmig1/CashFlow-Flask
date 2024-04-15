from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, union_all

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cashflow'
db = SQLAlchemy(app)

class Receitas(db.Model):
    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date)
    valor = db.Column(db.Integer)
    descricao = db.Column(db.String(150))
  #  id_usuario(db.Column(db.foreng_key (Usuario.id_usuario))

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
    # Crie as seleções SQL para cada consulta
    selecao_despesas = Despesas.query.all()
    selecao_receitas = Receitas.query.all()
    dados = []
    for receita in selecao_receitas:
        dados.append(receita)

    for despesa in selecao_despesas:
        dados.append(despesa)

    return render_template('Listagem.html', despesas=selecao_despesas, receitas=selecao_receitas, tudo=dados)

@app.route('/config')
def config():
    return render_template('Config.html')

@app.route('/cadastro')
def cadastro():
    return render_template('CadastroListagem.html')

if __name__ == '__main__':
    app.run(debug=True)
