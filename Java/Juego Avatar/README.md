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


Clase 3 – Sistema de ataques y reglas del juego

En esta etapa del proyecto se desarrolló el sistema de combate entre el jugador y el enemigo. Se implementaron diferentes ataques (Puño, Patada y Barrida) y se establecieron las reglas de enfrentamiento entre ellos.

Cada vez que el jugador selecciona un ataque, el enemigo genera automáticamente un ataque aleatorio. Luego, el sistema compara ambos ataques para determinar si el resultado es victoria, derrota o empate, mostrando un mensaje dinámico en pantalla.

Además, se agregó una sección de reglas del juego para que el usuario pueda consultar cómo funciona la mecánica antes o durante la partida, sin afectar la experiencia de juego.

Funcionalidades implementadas:
Sistema de ataques del jugador (Puño, Patada, Barrida).
Generación aleatoria del ataque enemigo.
Comparación de ataques mediante estructuras condicionales.
Sistema de resultados: ganar, perder o empate.
Creación de mensajes dinámicos en pantalla.
Sección de reglas del juego.
Explicación de vidas del jugador y del enemigo.
Descripción de ventajas entre ataques:
Patada vence a Puño.
Puño vence a Barrida.
Barrida vence a Patada.