Juego Avatar – Desarrollo del Proyecto
Descripción del proyecto


Este proyecto consiste en el desarrollo de un juego inspirado en Avatar, realizado con HTML, CSS y JavaScript. El objetivo es que el jugador pueda seleccionar un personaje, mientras que la computadora elige uno de forma aleatoria para comenzar la partida.

Durante las diferentes clases se fueron incorporando funcionalidades para mejorar la interacción del usuario y la lógica del juego.



Clase 1 – Selección del personaje del jugador

En esta clase se desarrolló el sistema de selección del personaje del jugador. Se implementaron botones de selección (radio buttons) para elegir entre distintos personajes del universo Avatar: Zuko, Katara, Aang y Toph.

Además, se trabajó con estructuras de control (if / else if) para identificar qué personaje fue seleccionado y mostrarlo mediante un mensaje al usuario. También se agregó una validación para evitar continuar si el jugador no selecciona ningún personaje.

Funcionalidades implementadas:
Selección de personaje del jugador.
Identificación del personaje elegido.
Mensaje de confirmación de selección.
Validación de error si no se selecciona un personaje.



Clase 2 – Selección del personaje enemigo

En la siguiente etapa del proyecto se agregó la lógica para que la computadora seleccione un personaje enemigo de forma aleatoria.

Para ello, se utilizó Math.random() junto con Math.floor() para generar un número aleatorio entre 1 y 4, asociando cada número a un personaje diferente. Luego, el personaje enemigo fue almacenado en una variable y mostrado tanto mediante un mensaje como en pantalla utilizando innerHTML.

Funcionalidades implementadas:
Selección aleatoria del enemigo.
Uso de números aleatorios en JavaScript.
Asignación del personaje enemigo.
Visualización del personaje enemigo en pantalla.
Organización de funciones para respetar el flujo del juego.

Actualmente el juego permite seleccionar un personaje para el jugador y generar automáticamente un personaje enemigo, mostrando ambas selecciones correctamente en pantalla.


Clase 3 - 

Lo primero que hacemos hoy dia es cambiar los botones de fuego, agua, aire y tierra, por solo tres botones que ponemos Puño, Patada y Barrida, que seria como el ataque. Luego chequeamos que el personaje del enemigo se ponga aleatorio al nosotros seleccionar el personaje.
