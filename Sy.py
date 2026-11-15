import flask as fk
import os
from contextlib import closing
import sqlite3 as sq
Sy = fk.Flask(__name__)


try:
    con = sq.connect('arq.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, autor TEXT NOT NULL, nome_musica TEXT NOT NULL, musica TETX NOT NULL)')
except Exception as e:
    print(f"Erro ao criar banco: {e}")
    
    
def gravar(autor, nome_musica, musica):
    with closing(sq.connect('arq.db')) as con:
        with con:
            cur = con.cursor()
            cur.execute("""INSERT INTO usuarios (autor, nome_musica, musica) VALUES (?, ?, ?)""", (autor, nome_musica, musica))
            
def ler(id):
    with closing(sq.connect('arq.db')) as con:
        if id == -1:
            with con:
                cur = con.cursor()
                cur.execute("""SELECT COUNT(autor) FROM usuarios""")
                r = cur.fetchone()[0]
        elif id != 0:
            with con:
                cur = con.cursor()
                cur.execute("""SELECT autor, nome_musica, musica FROM usuarios WHERE id = ?""", (id))
                r = cur.fetchall()
        else:
            with con:
                cur = con.cursor()
                cur.execute("""SELECT autor, nome_musica, musica FROM usuarios""")
                r = cur.fetchall()
    return r

@Sy.route('/upload', methods = ['POST', 'GET'])
def upload():
 
    if fk.request.method == 'POST':
        arquivo = fk.request.files['Arquivo']
        autor = fk.request.form['autor']
        nome_musica = fk.request.form['musicaform']
    
        filename = arquivo.filename
        arquivo.save(filename)
        extensao = os.path.splitext(filename)
        nome = nome_musica + extensao[1]
        # os.rename(filename, nome)
        
        uploads = f"Uploads\\{filename}"
        os.replace(filename, uploads)
        
        gravar(autor, nome_musica, filename)
        
        return fk.render_template('upload.html')
    else:
        return fk.render_template('upload.html') 

@Sy.route('/musicas', methods = ['POST', 'GET'])
def musicas():
    Nmusicas = ler(-1)
    arquivos = ler(0)
    
    return fk.render_template('musicas.html', arquivos = arquivos, Nmusicas = Nmusicas)

@Sy.route('/musicas/<caminho>')
def download(caminho):
    uploads = f"Uploads\\"
    return fk.send_from_directory(uploads, caminho, as_attachment=True)
    

if __name__ == '__main__':
    Sy.run(debug=True)