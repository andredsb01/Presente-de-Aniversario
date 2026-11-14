import flask as fk
import os
import json

Sy = fk.Flask(__name__)
dados = 'config.json'

def num_musicas():
    if os.path.exists(dados):
        with open(dados, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"Musicas": 0}

def salvar(v):
    with open(dados, 'w', encoding='utf-8') as f:
        json.dump(v, f, indent=4, ensure_ascii=False)
        
num_musicas()

@Sy.route('/', methods = ['POST', 'GET'])
def name():
    x = num_musicas()
    nome = f"musica{x['Musicas']}"
    if fk.request.method == 'POST':
        arquivo = fk.request.files['Arquivo']
        filename = arquivo.filename
        arquivo.save(filename)
        extensao = os.path.splitext(filename)
        nome = nome + extensao[1]
        os.rename(filename, nome)
        uploads = f"Uploads\\{nome}"
        os.replace(nome, uploads)
        x['Musicas'] += 1
        salvar(x)
        return fk.render_template('pagina1.html')
    else:
        return fk.render_template('pagina1.html') 



if __name__ == '__main__':
    Sy.run(debug=True)