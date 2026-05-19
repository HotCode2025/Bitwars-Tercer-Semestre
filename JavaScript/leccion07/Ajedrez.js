
// PROBLEMA DE LAS N REINAS — Backtracking

/**
 * Verifica si es seguro colocar una reina
 * en la posición (row, col) del tablero.
 * @param {number[]} board - Arreglo de columnas por fila
 * @param {number} row - Fila actual
 * @param {number} col - Columna a probar
 * @returns {boolean}
 */
function isSafe(board, row, col) {
  for (let r = 0; r < row; r++) {
    // Misma columna
    if (board[r] === col) return false;
    // Diagonal
    if (Math.abs(board[r] - col) === Math.abs(r - row)) return false;
  }
  return true;
}

/**
 * Función recursiva de backtracking.
 * @param {number[]} board - Estado actual del tablero
 * @param {number} row - Fila actual a procesar
 * @param {number} N - Tamaño del tablero
 * @param {number[][]} solutions - Array donde se guardan soluciones
 */
function solve(board, row, N, solutions) {
  // Caso base: todas las filas tienen reina → solución encontrada
  if (row === N) {
    solutions.push([...board]);
    return;
  }
  // Probar cada columna en la fila actual
  for (let col = 0; col < N; col++) {
    if (isSafe(board, row, col)) {
      board[row] = col;       // Colocar reina
      solve(board, row + 1, N, solutions); // Avanzar
      board[row] = -1;        // Backtrack: quitar reina
    }
  }
}

/**
 * Función principal: resuelve el problema para N reinas.
 * @param {number} N - Tamaño del tablero (mínimo 8)
 * @returns {number[][]} - Array de soluciones
 */
function nReinas(N) {
  if (N < 1) throw new Error("N debe ser mayor a 0");
  const board = new Array(N).fill(-1);
  const solutions = [];
  solve(board, 0, N, solutions);
  return solutions;
}


// EJEMPLO DE USO
const N = 8;
const soluciones = nReinas(N);

console.log(`Soluciones para N=${N}: ${soluciones.length}`);
// → Soluciones para N=8: 92

console.log("Primera solución (columna por fila):", soluciones[0]);
// → [0, 4, 7, 5, 2, 6, 1, 3]

function mostrarTablero(solucion) {
  const n = solucion.length;
  console.log("\nTablero:");
  for (let r = 0; r < n; r++) {
    let fila = "";
    for (let c = 0; c < n; c++) {
      fila += solucion[r] === c ? " ♛ " : " · ";
    }
    console.log(fila);
  }
}

mostrarTablero(soluciones[0]);