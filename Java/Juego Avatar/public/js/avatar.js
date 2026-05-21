let inputZuko = document.getElementById('zuko')
let inputKatara = document.getElementById('katara')
let inputAang = document.getElementById('aang')
let inputToph = document.getElementById('toph')


function seleccionarPersonajeJugador(){
    if (inputZuko.checked) {
        alert("Seleccionaste Zuko")
    } else if(inputKatara.checked){
        alert("Seleccionaste Katara")
    } else if(inputAang.checked){
        alert("Seleccionaste Aang")
    } else if(inputToph.checked){
        alert("Seleccionaste Toph")
    } else{
        alert("Error: debes elegir un personaje")
    }
}

let botonPersonajeJugador = document.getElementById('boton-personaje');
botonPersonajeJugador.addEventListener('click', seleccionarPersonajeJugador);
