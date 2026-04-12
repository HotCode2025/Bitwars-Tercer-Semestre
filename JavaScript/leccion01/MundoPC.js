// ============================================================
// PARTE 1 DispositivoEntrada
// Representa cualquier dispositivo que se conecta a una PC.

class DispositivoEntrada {

  // El constructor se ejecuta cuando creamos un objeto nuevo.
  // Recibe el tipo de conexion (USB, Bluetooth, etc.) y la marca.
  constructor(tipoEntrada, marca) {
    this.tipoEntrada = tipoEntrada; // guarda el tipo en el objeto
    this.marca = marca;             // guarda la marca en el objeto
  }

  // GETTERS: metodos para leer los atributos desde afuera
  getTipoEntrada() { return this.tipoEntrada; }
  getMarca()       { return this.marca; }

  // SETTERS: metodos para modificar los atributos desde afuera
  setTipoEntrada(t) { this.tipoEntrada = t; }
  setMarca(m)       { this.marca = m; }
}


// ============================================================
// PARTE 2 Raton
// Hereda todo de DispositivoEntrada usando "extends".
// Agrega su propio id unico y un metodo toString().

class Raton extends DispositivoEntrada {

  // "static" significa que este contador pertenece a la CLASE,
  // no a cada objeto. Asi todos los ratones comparten el mismo
  // contador y cada uno recibe un id diferente.
  static contadorRatones = 0;

  constructor(tipoEntrada, marca) {
    // "super" llama al constructor del padre (DispositivoEntrada)
    // para que inicialice tipoEntrada y marca. Es obligatorio
    // cuando usamos "extends".
    super(tipoEntrada, marca);

    Raton.contadorRatones++;                  // incrementa el contador global
    this.idRaton = Raton.contadorRatones;     // asigna el id a este objeto
  }

  // toString() devuelve una descripcion del objeto en texto.
  // Las comillas invertidas `` permiten meter variables con ${}
  toString() {
    return `Raton #${this.idRaton} | tipo: ${this.tipoEntrada} | marca: ${this.marca}`;
  }
}


// ============================================================
// PARTE 3 Teclado
// Igual que Raton, hereda de DispositivoEntrada.
// Tiene su propio contador e id independiente al del Raton.

class Teclado extends DispositivoEntrada {

  static contadorTeclado = 0; // contador exclusivo para teclados

  constructor(tipoEntrada, marca) {
    super(tipoEntrada, marca); // inicializa lo heredado del padre

    Teclado.contadorTeclado++;
    this.idTeclado = Teclado.contadorTeclado;
  }

  toString() {
    return `Teclado #${this.idTeclado} | tipo: ${this.tipoEntrada} | marca: ${this.marca}`;
  }
}


// ============================================================
// PARTE 4 Monitor
// No hereda de nadie. Es su propia clase separada.
// Solo tiene getter para el id (no se puede cambiar desde afuera).

class Monitor {

  static contadorMonitores = 0; // contador exclusivo para monitores

  constructor(marca, tamanio) {
    Monitor.contadorMonitores++;
    this.idMonitor = Monitor.contadorMonitores; // id autoincremental
    this.marca     = marca;
    this.tamanio   = tamanio;
  }

  // Solo getter para idMonitor, sin setter.
  // El id no deberia modificarse una vez creado el objeto.
  getIdMonitor() { return this.idMonitor; }

  toString() {
    return `Monitor #${this.idMonitor} | marca: ${this.marca} | tamanio: ${this.tamanio}`;
  }
}


// ============================================================
// PARTE 5 Computadora
// No hereda de nadie, pero CONTIENE objetos de otras clases.
// Recibe un Monitor, un Teclado y un Raton ya creados.
// Esto se llama AGREGACION (el diamante del diagrama UML).

class Computadora {

  static contadorComputadoras = 0;

  // Recibe los objetos ya creados como parametros,
  // no los crea internamente. Por eso es "agregacion".
  constructor(nombre, monitor, teclado, raton) {
    Computadora.contadorComputadoras++;
    this.idComputadora = Computadora.contadorComputadoras;
    this.nombre  = nombre;
    this.monitor = monitor; // objeto de tipo Monitor
    this.teclado = teclado; // objeto de tipo Teclado
    this.raton   = raton;   // objeto de tipo Raton
  }

  // Llama al toString() de cada objeto interno para mostrar
  // toda la informacion de la computadora en una sola linea.
  // \n es salto de linea, -> es solo decoracion visual.
  toString() {
    return `PC #${this.idComputadora} "${this.nombre}"
  -> ${this.monitor.toString()}
  -> ${this.teclado.toString()}
  -> ${this.raton.toString()}`;
  }
}


// ============================================================
// PARTE 6 Orden
// Es el nivel mas alto del sistema.
// Contiene un ARREGLO de objetos Computadora.
// Se pueden ir agregando computadoras una por una.

class Orden {

  static contadorOrdenes = 0;

  constructor() {
    Orden.contadorOrdenes++;
    this._idOrden = Orden.contadorOrdenes; // el _ indica que es "privado" por convencion
    this.computadoras = [];                // empieza como arreglo vacio
  }

  // Agrega una computadora al arreglo usando push()
  agregarComputadora(c) {
    this.computadoras.push(c);
  }

  // Recorre todas las computadoras del arreglo y
  // arma un resumen completo de la orden con forEach()
  mostrarOrden() {
    let r = `=== ORDEN #${this._idOrden} ===\n`;

    // forEach recorre cada elemento del arreglo.
    // "c" representa cada computadora en cada vuelta.
    this.computadoras.forEach(c => {
      r += c.toString() + "\n\n"; // agrega la info de cada PC
    });

    r += `Total: ${this.computadoras.length} computadoras`;
    return r;
  }
}


// ============================================================
// PARTE 7 PRUEBAS
// Aca creamos los objetos en el orden correcto:
// primero los perifericos, luego la PC, luego la orden.

// Computadora 1
const mon1 = new Monitor("xiaomi", '24"');
const tec1 = new Teclado("USB", "Redragonborn");
const rat1 = new Raton("dongle inalambrico", "ATK A9plus");
const pc1  = new Computadora("PC Gamer", mon1, tec1, rat1);

// Computadora 2
const mon2 = new Monitor("Philips", '24"');
const tec2 = new Teclado("USB", "Redragon Kumara");
const rat2 = new Raton("USB", "logitech GPRO");
const pc2  = new Computadora("Pc mac", mon2, tec2, rat2);

// Orden
const orden = new Orden();
orden.agregarComputadora(pc1);
orden.agregarComputadora(pc2);

// Mostramos el resumen completo en consola
console.log(orden.mostrarOrden());