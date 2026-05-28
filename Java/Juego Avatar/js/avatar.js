function iniciarJuego(){
    let botonPersonajeJugador = document.getElementById('boton-personaje');
botonPersonajeJugador.addEventListener('click', seleccionarPersonajeJugador);
}

let personajeEnemigo

function seleccionarPersonajeJugador(){
    let inputZuko = document.getElementById('zuko')
    let inputKatara = document.getElementById('katara')
    let inputAang = document.getElementById('aang')
    let inputToph = document.getElementById('toph')
    let spanPersonajeJugador = document.getElementById('personaje-jugador')

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
    }

    aleatoria()
} 

function aleatoria() {
    let spanPersonajeEnemigo = document.getElementById('personaje-enemigo')
    let personajePC = Math.floor(Math.random() * (4 - 1 + 1)+ 1)

    if (personajePC == 1) {
        personajeEnemigo = 'Zuko'
        alert('El personaje del enemigo es Zuko')
    } else if (personajePC == 2) {
        personajeEnemigo = 'Katara'
        alert('El personaje del enemigo es Katara')
    } else if (personajePC == 3) {
        personajeEnemigo = 'Aang'
        alert('El personaje del enemigo es Aang')
    } else {
        personajeEnemigo = 'Toph'
        alert('El personaje del enemigo es Toph')
    }

    spanPersonajeEnemigo.innerHTML = personajeEnemigo
    alert('El personaje del enemigo es ' + personajeEnemigo)
}

window.addEventListener('load', iniciarJuego)


