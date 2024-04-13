from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def entrar():
    return render_template('Entrar.html')

@app.route('/geral')
def geral():
    return render_template('Geral.html')

@app.route('/listagem')
def listagem():
    return render_template('Listagem.html')

@app.route('/config')
def config():
    return render_template('Config.html')

@app.route('/cadastro')
def cadastro():
    return render_template('CadastroListagem.html')

if __name__ == '__main__':
    app.run(debug=True)
