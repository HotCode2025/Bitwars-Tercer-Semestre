let torres = {
  A: [],
  B: [],
  C: []
};

let movimientos = [];
let velocidad = 700;

function iniciarJuego() {
  let cantidad = parseInt(document.getElementById("cantidadDiscos").value);

  torres = {
    A: [],
    B: [],
    C: []
  };

  movimientos = [];

  for (let i = cantidad; i >= 1; i--) {
    torres.A.push(i);
  }

  document.getElementById("movimiento").innerHTML = "Juego iniciado";
  dibujarTorres();
}

function dibujarTorres() {
  let nombresTorres = ["A", "B", "C"];

  nombresTorres.forEach(nombre => {
    let poste = document.getElementById(nombre);

    poste.innerHTML = `
      <div class="palo"></div>
      <h2>${nombre}</h2>
    `;

    torres[nombre].forEach(disco => {
      let div = document.createElement("div");
      div.classList.add("disco");

      div.style.width = `${disco * 30 + 50}px`;
      div.style.background = obtenerColor(disco);
      div.innerHTML = disco;

      poste.appendChild(div);
    });
  });
}

function obtenerColor(numero) {
  let colores = [
    "#ef4444",
    "#f97316",
    "#eab308",
    "#22c55e",
    "#06b6d4",
    "#3b82f6",
    "#8b5cf6"
  ];

  return colores[numero - 1];
}

function resolverHanoi() {
  iniciarJuego();

  let cantidad = parseInt(document.getElementById("cantidadDiscos").value);

  hanoi(cantidad, "A", "C", "B");

  ejecutarMovimientos(0);
}

function hanoi(n, origen, destino, auxiliar) {
  if (n === 1) {
    movimientos.push({
      origen: origen,
      destino: destino
    });
  } else {
    hanoi(n - 1, origen, auxiliar, destino);

    movimientos.push({
      origen: origen,
      destino: destino
    });

    hanoi(n - 1, auxiliar, destino, origen);
  }
}

function ejecutarMovimientos(indice) {
  if (indice >= movimientos.length) {
    document.getElementById("movimiento").innerHTML = "¡Juego terminado!";
    return;
  }

  let mov = movimientos[indice];

  let disco = torres[mov.origen].pop();
  torres[mov.destino].push(disco);

  document.getElementById("movimiento").innerHTML =
    `Movimiento ${indice + 1}: disco ${disco} de ${mov.origen} a ${mov.destino}`;

  dibujarTorres();

  setTimeout(() => {
    ejecutarMovimientos(indice + 1);
  }, velocidad);
}