import os
from flask import Flask, redirect
import random
import pymongo
import json
from flask import jsonify, request
from bson import ObjectId
from bson.json_util import dumps

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = pymongo.MongoClient("mongodb+srv://admin-tateti:admin@tateti-hgpwu.mongodb.net/test?retryWrites=true&w=majority")
db = client.tateti
collection = db.partidas


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

@app.route("/partidas")
def get_partidas():
    partidas = collection.find()
    resp = dumps(partidas)
    return resp

@app.route('/partida/<id>', methods=['GET'])
def get_partida(id):
    partida = collection.find_one({'_id': ObjectId(id)})
    resp = dumps(partida)
    return resp


@app.route('/nueva_partida', methods=['POST'])
def nueva_partida():
    _json = request.json
    _jugador = _json["jugador"]
    _forma = _json["forma"]
    _add_date = _json["add_date"]
    # a partir de la forma seleccionada obtengo a la de la maquina
    if _forma == "X":
        forma_maq = "O"
    else:
        forma_maq = "X"

    # valido los valores recibidos
    if _jugador and _forma and _add_date and request.method == 'POST':
        id = collection.insert({"jugador": _jugador, "add_date": _add_date, "forma": _forma, "forma_maq": forma_maq, "tablero":",,,,,,,,", "ganador":""})
        resp = jsonify("Nueva partida con id {} generada".format(id))
        resp.status_code = 200
    return redirect('/partida/{}'.format(id))


@app.route('/partida/<id>/jugar/<int:pos>')
def jugada_humano(id, pos):
    partida = collection.find_one({'_id': ObjectId(id)})
    partida = dumps(partida)
    partida = json.loads(partida)

    #convierto en lista para tratarlo mas facil
    tab = partida["tablero"].split(",")

    #valido que no este ocupado ya la posicion
    if tab[pos] != '':
        return {"error": "Ya esta ocupada la posicion donde quiere jugar."}
    #valido posicion dentro de rango 0 a 8
    if pos < 0 or pos > 8:
        return {"error": "Posicion fuera de rango, debe ser un entero dentro de 0 y 8 inclusive"}

    tab[pos] = partida["forma"]
    partida["tablero"] = ",".join(tab)

    collection.update_one({"_id": ObjectId(id)}, {"$set": { "tablero": partida["tablero"] }})
    # verifico si gano el humano
    if hay_ganador(partida["tablero"]):
        partida["ganador"] = partida["jugador"]
        collection.update_one({"_id": ObjectId(id)}, {"$set": { "ganador": partida["ganador"] }})
        return redirect('/partida/{}'.format(id))
    if tablero_lleno(partida["tablero"]):
        partida["ganador"] = "Tablero lleno, hay un empate."
        collection.update_one({"_id": ObjectId(id)}, {"$set": { "ganador": partida["ganador"] }})
        return redirect('/partida/{}'.format(id))

    return redirect('/partida/{}/juega_maquina'.format(id))


@app.route('/partida/<id>/juega_maquina')
def maquina(id):
    partida = collection.find_one({'_id': ObjectId(id)})
    partida = dumps(partida)
    partida = json.loads(partida)

    partida["tablero"] = jugada_maquina(partida["tablero"])
    collection.update_one({"_id": ObjectId(id)}, {"$set": { "tablero": partida["tablero"] }})
    # verifico si gano la maquina
    if hay_ganador(partida["tablero"]):
        partida["ganador"] = "Maquina Wall-e"
        collection.update_one({"_id": ObjectId(id)}, {"$set": { "tablero": partida["tablero"], "ganador": partida["ganador"] }})
        return redirect('/partida/{}'.format(id))
    if tablero_lleno(partida["tablero"]):
        partida["ganador"] = "Tablero lleno, hay un empate."
        collection.update_one({"_id": ObjectId(id)}, {"$set": { "tablero": partida["tablero"], "ganador": partida["ganador"] }})
        return redirect('/partida/{}'.format(id))

    return redirect('/partida/{}'.format(id))



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
