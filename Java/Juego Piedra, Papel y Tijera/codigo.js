// CONTADOR DE VICTORIAS
let victoriasJugador = 0
let victoriasPC = 0

// MOSTRAR BOTONES DE OPCIONES
function mostrarOpciones() {

    // MOSTRAR OPCIONES
    document.getElementById("opciones").style.display = "block"

    // OCULTAR BOTON JUGAR
    document.getElementById("botonJugar").style.display = "none"
}

// FUNCION PRINCIPAL
function jugar(jugador) {

    // NUMERO ALEATORIO DE LA PC
    let pc = Math.floor(Math.random() * (3 - 1 + 1) + 1)

    // VARIABLES
    let eleccionJugador = ""
    let eleccionPC = ""
    let resultado = ""

    // ELECCION DEL JUGADOR
    if (jugador == 1) {

        eleccionJugador = "🪨 Piedra"

    } else if (jugador == 2) {

        eleccionJugador = "📄 Papel"

    } else {

        eleccionJugador = "✂️ Tijera"
    }

    // ELECCION DE LA PC
    if (pc == 1) {

        eleccionPC = "🪨 Piedra"

    } else if (pc == 2) {

        eleccionPC = "📄 Papel"

    } else {

        eleccionPC = "✂️ Tijera"
    }

    // COMBATE
    if (pc == jugador) {

        resultado = "🤝 EMPATE"

    } else if (jugador == 1 && pc == 3) {

        resultado = "🎉 GANASTE"

        // SUMAR PUNTO
        victoriasJugador++

    } else if (jugador == 2 && pc == 1) {

        resultado = "🎉 GANASTE"

        // SUMAR PUNTO
        victoriasJugador++

    } else if (jugador == 3 && pc == 2) {

        resultado = "🎉 GANASTE"

        // SUMAR PUNTO
        victoriasJugador++

    } else {

        resultado = "💀 PERDISTE"

        // SUMAR PUNTO A LA PC
        victoriasPC++
    }

    // ACTUALIZAR PUNTAJE
    document.getElementById("puntosJugador").innerHTML =
        victoriasJugador

    document.getElementById("puntosPC").innerHTML =
        victoriasPC

    // MOSTRAR RESULTADO
    document.getElementById("resultado").innerHTML =

        "Elegiste: " + eleccionJugador +

        "<br>La PC eligió: " + eleccionPC +

        "<br><br><strong>" + resultado + "</strong>"

    // SI EL JUGADOR GANA
    if (victoriasJugador == 3 || victoriasPC == 3) {

        // OCULTAR OPCIONES
        document.getElementById("opciones").style.display =
            "none"

        // MOSTRAR BOTON REINICIAR
        document.getElementById("botonReiniciar").style.display =
            "block"

        // MENSAJE FINAL
        if (victoriasJugador == 3) {

            document.getElementById("resultado").innerHTML +=

                "<br><br>🏆 GANASTE LA PARTIDA"

        } else {

            document.getElementById("resultado").innerHTML +=

                "<br><br>💻 LA PC GANÓ LA PARTIDA"
        }
    }
}

// REINICIAR PARTIDA
function reiniciarJuego() {

    // VOLVER PUNTAJES A 0
    victoriasJugador = 0
    victoriasPC = 0

    // ACTUALIZAR MARCADOR
    document.getElementById("puntosJugador").innerHTML = 0

    document.getElementById("puntosPC").innerHTML = 0

    // MENSAJE INICIAL
    document.getElementById("resultado").innerHTML =

        "¡Comienza la partida!"

    // MOSTRAR BOTON JUGAR
    document.getElementById("botonJugar").style.display =
        "block"

    // OCULTAR BOTON REINICIAR
    document.getElementById("botonReiniciar").style.display =
        "none"
}