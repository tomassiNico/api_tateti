import os
from flask import Flask, redirect
import random

app = Flask(__name__)

partida = {"jugador":"Luis Alberto", "forma":"X", "tablero":",,,,,,,,", "ganador":""}

def hay_ganador(tablero):
    #paso de string a lista
    tab = tablero.split(",")
    #genero lista con combinaciones ganadoras
    pos_ganadoras = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

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

def tablero_lleno(tablero):
    tab = tablero.split(",")

    # itero cada posicion, si hay una posicion vacia retorno False ya que no esta lleno
    for pos in tab:
        if pos == '':
            return False
    # si itero todos y no encontro lugar vacio esta lleno por lo tanto retorno True
    return True

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


@app.route('/partida/jugar/<int:pos>')
def jugada_humano(pos):
    tab = partida["tablero"].split(",")

    #valido que no este ocupado ya la posicion
    if tab[pos] != '':
        return {"error": "Ya esta ocupada la posicion donde quiere jugar."}
    #valido posicion dentro de rango 0 a 8
    if pos < 0 or pos > 8:
        return {"error": "Posicion fuera de rango, debe ser un entero dentro de 0 y 8 inclusive"}

    tab[pos] = "X"
    partida["tablero"] = ",".join(tab)

    # verifico si gano el humano
    if hay_ganador(partida["tablero"]):
        partida["ganador"] = partida["jugador"]
        return redirect('/partida')
    if tablero_lleno(partida["tablero"]):
        partida["ganador"] = "Tablero lleno, hay un empate."
        return redirect('/partida')

    return redirect('/partida/juega_maquina')


@app.route('/partida/juega_maquina')
def maquina():
    partida["tablero"] = jugada_maquina(partida["tablero"])

    # verifico si gano la maquina
    if hay_ganador(partida["tablero"]):
        partida["ganador"] = "Maquina Wall-e"
    if tablero_lleno(partida["tablero"]):
        partida["ganador"] = "Tablero lleno, hay un empate."
        return redirect('/partida')

    return redirect('/partida')



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
