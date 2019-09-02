# API RESTful Ta-Te-Ti

API para jugar al Ta-Te-Ti !

Juega una partida del mismo en:
https://frozen-wave-46424.herokuapp.com/

El código de un proyecto complementario donde se consume la API expuesta es en:
https://github.com/tomassiNico/web_api_tateti

## Funcionalidades expuestas:

  * Crear nueva partida
  * Jugar una partida contra la PC
  * Observa el historico de partidas jugadas

## Cómo utilizar:

### Crear nueva partida
Tipo de mensaje HTTP: POST<br/>
Parametros: Archivo en formato JSON. 
  * jugador: nombre del jugador.
  * add_date: fecha de creación de la partida.
  * forma: forma que elije para jugar. Valores posibles: 'X' y 'O'

Ejemplo:
```
{ "jugador": "Luis Alberto Spinetta",
  "add_date": "08/23/2019 19:70:30",
  "forma": "X" 
}
```
Endpoint: 
```
https://murmuring-forest-97474.herokuapp.com/nueva_partida
```
Retorna:
Archivo JSON con datos de la partida:
  * id
  * jugador
  * forma
  * forma_maq
  * add_date
  * tablero
  * ganador
  
### Detalle de una partida
Tipo de mensaje HTTP: GET<br/>

Endpoint: 
```
https://murmuring-forest-97474.herokuapp.com/partida/<id>
```
Parámetro:
  * id: id de la partida

Retorna:
Archivo JSON con datos de la partida:
  * id
  * jugador
  * forma
  * forma_maq
  * add_date
  * tablero
  * ganador

### Jugar / Realizar un movimiento
Tipo de mensaje HTTP: GET<br/>

Endpoint: 
```
https://murmuring-forest-97474.herokuapp.com/partida/<id>/jugar/<pos>
```
Parámetros:
  * id: id de la partida
  * pos: posicion donde se quiere marcar el tablero (número entero de 0 a 8 inclusive)

Retorna:,<br/>
Archivo JSON con datos de la partida, con el tablero marcado en la posición solicitada y la respuesta de la maquina.

### Solicitar que la PC juegue
Tipo de mensaje HTTP: GET<br/>

Endpoint: 
```
https://murmuring-forest-97474.herokuapp.com/partida/<id>/jugar/<pos>
```
Parámetros:
  * id: id de la partida

Retorna:,<br/>
Archivo JSON con datos de la partida, con el tablero marcado en la posición seleccionada por la maquina.


### Obtener todas las partidas.
Tipo de mensaje HTTP: GET

Endpoint: 
```
https://murmuring-forest-97474.herokuapp.com/partidas
```
Retorna:
Archivo JSON con datos de todas las partidas.


