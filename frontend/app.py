from tabnanny import check

from flask import Flask, request, render_template, session, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2._psycopg import cursor
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta_segura'


DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

print("DATABASE_URL:", DATABASE_URL)



@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor.execute("SELECT id, senha FROM cuidadores WHERE email = %s", (email,))
        cuidador = cursor.fetchone()

        if cuidador and check_password_hash(cuidador[1], senha):
            session['cuidador_id'] = cuidador[0]
            return redirect(url_for('dashboard'))
        return "Login inválido!"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('cuidador_id', None)
    return redirect(url_for('login'))


@app.route('/cadastro_cuidador', methods=['GET', 'POST'])
def cadastro_cuidador():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        senha_hash = generate_password_hash(senha)

        cursor.execute("""
                       INSERT INTO cuidadores (nome, email,  senha) VALUES (%s, %s, %s) 
                       """, (nome, email,  senha_hash))
        conn.commit()
        return redirect(url_for('login'))

    return render_template('cadastro_cuidador.html')

@app.route('/dashboard')
def dashboard():
    if 'cuidador_id' not in session:
        return redirect(url_for('login'))

    cuidador_id = session['cuidador_id']
    cursor.execute('SELECT * FROM pacientes WHERE cuidador_id = %s', (cuidador_id,))
    pacientes = cursor.fetchall()

    return render_template('dashboard.html', pacientes=pacientes)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if 'cuidador_id' not in session:
        return redirect(url_for('login'))
    else:
        cuidador_id = session['cuidador_id']
        nome = request.form['nome_completo']
        data_nasc = request.form['data_nascimento']
        sexo = request.form['sexo']
        cpf = request.form['cpf']
        tel = request.form['telefone']
        email = request.form['email']
        estado_civil = request.form['est_civ']
        nome_mae = request.form['n_mae']
        nome_pai = request.form['n_pai']
        nacionalidade = request.form['nacic']
        naturalidade = request.form['natu']
        contato_emergencia_nome = request.form['n_cont_emr']
        contato_emergencia_telefone = request.form['tel_cont_emr']
        contato_emergencia_parentesco = request.form['paren_cont_emr']
        endereco = request.form['end']
        cep = request.form['cep']
        tipo_sanguineo = request.form['tp_sangue']
        alergias = request.form['alergias']
        doencas_cronicas = request.form['doen_cro']
        medicamentos_em_uso = request.form['medic_uso']

        cursor.execute("""INSERT INTO pacientes (cuidador_id, nome, data_nasc, sexo, cpf, tel, email, estado_civil, nome_mae, nome_pai, nacionalidade,
                naturalidade, contato_emergencia_nome,  contato_emergencia_telefone, contato_emergencia_parentesco, endereco, 
                cep, tipo_sanguineo,  alergias, doencas_cronicas, medicamentos_em_uso )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (cuidador_id, nome, data_nasc, sexo, cpf, tel, email, estado_civil, nome_mae, nome_pai, nacionalidade,
                naturalidade, contato_emergencia_nome,  contato_emergencia_telefone, contato_emergencia_parentesco, endereco,
                cep, tipo_sanguineo,  alergias, doencas_cronicas, medicamentos_em_uso ))
        conn.commit()

        return redirect(url_for('dashboard'))

@app.route('/form')
def form():
    if 'cuidador_id' not in session:
        return redirect(url_for('login'))
    return render_template('form.html')

@app.route('/pacientes/<int:id>')

def detalhes_pacientes(id):
    cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
    paciente = cursor.fetchone()
    return render_template('detalhes_pacientes.html', paciente=paciente)


if __name__ == '__main__':
    app.run(debug=True)



