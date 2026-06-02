const N = 8;

let tablero = [];
let camino = [];

let movX = [2, 1, -1, -2, -2, -1, 1, 2];
let movY = [1, 2, 2, 1, -1, -2, -2, -1];

function crearTablero() {
    tablero = [];
    camino = [];

    for (let i = 0; i < N; i++) {
        tablero[i] = [];
        for (let j = 0; j < N; j++) {
            tablero[i][j] = -1;
        }
    }
}

function esValido(x, y) {
    return x >= 0 && x < N && y >= 0 && y < N && tablero[x][y] === -1;
}

function resolver(x, y, salto) {
    if (salto === N * N) {
        return true;
    }

    for (let i = 0; i < 8; i++) {
        let nuevoX = x + movX[i];
        let nuevoY = y + movY[i];

        if (esValido(nuevoX, nuevoY)) {
            tablero[nuevoX][nuevoY] = salto;
            camino.push({ x: nuevoX, y: nuevoY, salto: salto });

            if (resolver(nuevoX, nuevoY, salto + 1)) {
                return true;
            }

            tablero[nuevoX][nuevoY] = -1;
            camino.pop();
        }
    }

    return false;
}

function dibujarTablero(posicionCaballo = null, hastaSalto = -1) {
    let contenedor = document.getElementById("tablero");
    contenedor.innerHTML = "";

    for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
            let casilla = document.createElement("div");

            casilla.classList.add("casilla");

            if ((i + j) % 2 === 0) {
                casilla.classList.add("blanca");
            } else {
                casilla.classList.add("negra");
            }

            let numero = "";

            for (let k = 0; k <= hastaSalto; k++) {
                if (camino[k] && camino[k].x === i && camino[k].y === j) {
                    numero = camino[k].salto;
                }
            }

            if (
                posicionCaballo &&
                posicionCaballo.x === i &&
                posicionCaballo.y === j
            ) {
                casilla.innerHTML = "♞";
                casilla.classList.add("caballo");
            } else {
                casilla.textContent = numero;
            }

            contenedor.appendChild(casilla);
        }
    }
}

function animarCamino() {
    let paso = 0;

    let intervalo = setInterval(() => {
        let posicionActual = camino[paso];

        dibujarTablero(posicionActual, paso - 1);

        paso++;

        if (paso >= camino.length) {
            clearInterval(intervalo);

            setTimeout(() => {
                dibujarTablero(null, camino.length - 1);
            }, 500);
        }

    }, 500);
}

function iniciar() {
    crearTablero();

    tablero[0][0] = 0;
    camino.push({ x: 0, y: 0, salto: 0 });

    if (resolver(0, 0, 1)) {
        animarCamino();
    } else {
        alert("No se encontró solución");
    }
}