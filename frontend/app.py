from flask import Flask, request, render_template
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

print("DATABASE_URL:", DATABASE_URL)


cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
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

    cursor.execute("""
         INSERT INTO pacientes (nome, data_nasc, sexo, cpf, tel, email, estado_civil, nome_mae, nome_pai, nacionalidade,
            naturalidade, contato_emergencia_nome,  contato_emergencia_telefone, contato_emergencia_parentesco, endereco, 
            cep, tipo_sanguineo,  alergias, doencas_cronicas, medicamentos_em_uso )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, data_nasc, sexo, cpf, tel, email, estado_civil, nome_mae, nome_pai, nacionalidade,
            naturalidade, contato_emergencia_nome,  contato_emergencia_telefone, contato_emergencia_parentesco, endereco,
            cep, tipo_sanguineo,  alergias, doencas_cronicas, medicamentos_em_uso ))
    conn.commit()

    return "Paciente cadastrado com sucesso!"


@app.route('/listar')

def listar_pacientes():
    cursor.execute("SELECT id, nome FROM pacientes")
    pacientes = cursor.fetchall()
    return render_template('lista_pacientes.html', pacientes=pacientes)


if __name__ == '__main__':
    app.run(debug=True)



