class Animal {
  constructor(nombre, edad) {
    this.nombre = nombre;
    this.edad = edad;
  }
}

class Perro extends Animal {
  constructor(nombre, edad, raza) { // Parámetros
  super(nombre, edad)  // Heredados de Animal
    this.raza = raza;
}
}

let perro1 = new Perro("Firulais", 3, "Labrador"); // Llamada a la función

console.log(perro1) // Mostrar Perro1