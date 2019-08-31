import os
from flask import Flask, redirect

app = Flask(__name__)

partida = {"jugador":"Luis Alberto", "forma":"X", "tablero":",,,,,,,,,", "ganador":""}

@app.route("/")
def hello():
    return "Hello world!"

@app.route('/partida')
def get_partida():
    return partida

@app.route('/nueva_partida')
def nueva_partida():
    partida = {"jugador":"Luis Alberto", "forma":"X", "tablero":",,,,,,,,,", "ganador":""}
    return redirect('/partida')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
