from flask import Flask, render_template, request, redirect
import csv
import matplotlib.pyplot as plt
import os 

app = Flask(__name__)

CSV_FILE = "dados.csv"

# Carrega dados do CSV
def carregar_dados():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [int(row[0]) for row in reader]
    
# Salvar dados no CSV
def salvar_dados(valor):
    with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([valor])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lista')
def lista():
    dados = carregar_dados()
    total = sum(dados) if dados else 0
    media = total / len(dados) if dados else 0
    quantidade = len(dados)
    return render_template('lista.html', dados=dados, total=total, media=media, quantidade=quantidade)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        valor = request.form['valor']
        salvar_dados(valor)
        return redirect('/lista')
    return render_template('/cadastro.html')

@app.route('/grafico')
def grafico():
    dados = carregar_dados()

    if dados:
        plt.figure(figsize=(6,4))
        plt.plot(dados, marker='o')
        plt.title("Gráfico de Valores Cadastrados")
        plt.xlabel("Índice")
        plt.ylabel("Valor")
        plt.grid(True)
        plt.savefig("static/grafico.png")
        plt.close()

    return render_template('grafico.html')

app.run(debug=True)