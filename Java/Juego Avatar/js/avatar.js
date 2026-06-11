let ataqueJugador
let ataqueEnemigo
let vidasJugador = 3
let vidasEnemigo = 3

function iniciarJuego(){
    let sectionSeleccionarAtaque = document.getElementById('seleccionar-ataque')
    sectionSeleccionarAtaque.style.display = 'none'
    let botonPersonajeJugador = document.getElementById('boton-personaje')
    botonPersonajeJugador.addEventListener('click', seleccionarPersonajeJugador)
    let sectionReiniciar = document.getElementById('boton-reiniciar')
    sectionReiniciar.style.display = "none"

    let botonPunio = document.getElementById('boton-punio')
    botonPunio.addEventListener('click', ataquePunio)

    let botonPatada = document.getElementById('boton-patada')
    botonPatada.addEventListener('click', ataquePatada)

    let botonBarrida = document.getElementById('boton-barrida')
    botonBarrida.addEventListener('click', ataqueBarrida)

    let botonReglas = document.getElementById('reglasdejuego')
    botonReglas.addEventListener('click', mostrarOcultarReglas)
    //creamos una variable
    let botonReiniciar = document.getElementById('boton-reiniciar')
    botonReiniciar.addEventListener('click', reiniciarJuego)
}

function seleccionarPersonajeJugador(){
    let inputZuko = document.getElementById('zuko')
    let inputKatara = document.getElementById('katara')
    let inputAang = document.getElementById('aang')
    let inputToph = document.getElementById('toph')
    let spanPersonajeJugador = document.getElementById('personaje-jugador')

    let sectionSeleccionarAtaque = document.getElementById('seleccionar-ataque')
    sectionSeleccionarAtaque.style.display = 'block'
    let sectionSeleccionarPersonaje = document.getElementById('seleccionar-personaje')
    sectionSeleccionarPersonaje.style.display = 'none'

    if(inputZuko.checked){
        spanPersonajeJugador.innerHTML = 'Zuko'
    }else if(inputKatara.checked){
        spanPersonajeJugador.innerHTML = 'Katara'
    }else if(inputAang.checked){
        spanPersonajeJugador.innerHTML = 'Aang'
    }else if(inputToph.checked){
        spanPersonajeJugador.innerHTML = 'Toph'
    }else{
        alert('Selecciona a un personaje')
        reiniciarJuego()
        return
        
    }

    seleccionarPersonajeEnemigo()
} 

function seleccionarPersonajeEnemigo() {
    let personajeAleatorio = aleatorio(1,4)
    let spanPersonajeEnemigo = document.getElementById('personaje-enemigo')

    if (personajeAleatorio == 1) {
        spanPersonajeEnemigo.innerHTML = 'Zuko'
    } else if (personajeAleatorio == 2) {
        spanPersonajeEnemigo.innerHTML = 'Katara'
    } else if (personajeAleatorio == 3) {
        spanPersonajeEnemigo.innerHTML = 'Aang'
    } else {
        spanPersonajeEnemigo.innerHTML = 'Toph'
    }
}

function ataquePunio(){
    ataqueJugador = 'Puño'
    ataqueAleatorioEnemigo()
}

function ataquePatada(){
    ataqueJugador = 'Patada'
    ataqueAleatorioEnemigo()
}

function ataqueBarrida(){
    ataqueJugador = 'Barrida'
    ataqueAleatorioEnemigo()
}

function ataqueAleatorioEnemigo(){
    let ataqueAleatorio = aleatorio(1,3)

    if(ataqueAleatorio == 1){
        ataqueEnemigo = 'Puño'
    } else if(ataqueAleatorio == 2){
        ataqueEnemigo = 'Patada'
    } else {
        ataqueEnemigo = 'Barrida'
    }

    combate()
}

function combate(){
    let spanVidasJugador = document.getElementById('vidas-jugador')
    let spanVidasEnemigo = document.getElementById('vidas-enemigo')
    if (ataqueEnemigo == ataqueJugador) {
        crearMensaje("🤝 EMPATE")
    } else if (ataqueJugador == 'Puño' && ataqueEnemigo == 'Barrida') {
        crearMensaje("🎉 GANASTE")
        vidasEnemigo--
        spanVidasEnemigo.innerHTML = vidasEnemigo
    } else if (ataqueJugador == 'Patada' && ataqueEnemigo == 'Puño') {
        crearMensaje("🎉 GANASTE")
        vidasEnemigo--
        spanVidasEnemigo.innerHTML = vidasEnemigo
    } else if (ataqueJugador == 'Barrida' && ataqueEnemigo == 'Patada') {
        crearMensaje("🎉 GANASTE")
        vidasEnemigo--
        spanVidasEnemigo.innerHTML = vidasEnemigo
    } else {
        crearMensaje("💀 PERDISTE")
        vidasJugador--
        spanVidasJugador.innerHTML = vidasJugador
    }
    //Revisar vidas
    revisarVidas()
}

function revisarVidas(){
    if(vidasEnemigo == 0){
        //Ganamos
        crearMensajeFinal("FELICIDADES HAS GANADO!!!")
    }else if(vidasJugador == 0){
        //Perdimos
        crearMensajeFinal("QUE PENA HAS PERDIDO!!!")
    }
}

function crearMensajeFinal(resultado){
    let sectionReiniciar = document.getElementById('boton-reiniciar')
    sectionReiniciar.style.display = "block"

    let sectionMensaje = document.getElementById('mensajes')
    let parrafo = document.createElement('p')

    parrafo.innerHTML = resultado
 
    sectionMensaje.appendChild(parrafo)

    let botonPunio = document.getElementById('boton-punio')
    botonPunio.disabled = true

    let botonPatada = document.getElementById('boton-patada')
    botonPatada.disabled = true

    let botonBarrida = document.getElementById('boton-barrida')
    botonBarrida.disabled = true
}

function crearMensaje(resultado){
    let sectionMensaje = document.getElementById('mensajes')
    let parrafo = document.createElement('p')

    parrafo.innerHTML = 'Tu personaje atacó con ' + ataqueJugador + ' el personaje enemigo atacó con ' + ataqueEnemigo + ' ' + resultado

    sectionMensaje.appendChild(parrafo)
}

function mostrarOcultarReglas(){
    let seccionReglas = document.getElementById('reglas')
    let botonReglas = document.getElementById('reglasdejuego')

    if(seccionReglas.style.display == 'none' || seccionReglas.style.display == ''){
        seccionReglas.style.display = 'block'
        botonReglas.innerHTML = '📕 Ocultar reglas'
    } else {
        seccionReglas.style.display = 'none'
        botonReglas.innerHTML = '📖 Ver reglas'
    }
}

function reiniciarJuego(){
    location.reload()
}

function aleatorio(min, max){
    return Math.floor(Math.random() * (max - min + 1) + min)
}

window.addEventListener('load', iniciarJuego)