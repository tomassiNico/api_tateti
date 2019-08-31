import os
from flask import Flask, redirect
import random

app = Flask(__name__)

partida = {"jugador":"Luis Alberto", "forma":"X", "tablero":",,,,,,,,,", "ganador":""}

def hay_ganador(tablero):
    #paso de string a lista
    tab = tablero.split(",")
    #genero lista con combinaciones ganadoras
    pos_ganadoras = [[0,1,2],[3,4,5],[6.7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

    for pos in pos_ganadoras:
        if (tab[pos[0]] == '') or (tab[pos[1]] == '') or (tab[pos[2]] == ''):
            # si ingresa aca significa que hay al menos una posicion que esta vacia por lo tanto no hay posibilidad de ganar
            # sigo con la siguiente posible posicion ganadora
            continue
        if (tab[pos[0]] == tab[pos[1]] == tab[pos[2]]):
            return True
    return False

def jugada_maquina(tablero):
    #paso de string a lista
    tab = tablero.split(",")
    # bandera para verificar si la maquina hizo su jugada
    jugo = False
    while (not jugo):
        pos = random.randint(0,8)
        if (tab[pos] == ''):
            tab[pos] = "O"
            jugo = True
            #paso de lista a string
            tablero = ",".join(tab)
            return tablero
    

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
