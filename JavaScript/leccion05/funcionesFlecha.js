miFuncion();

function miFuncion(){
    console.log("Saludos desde mi funcion");

}
miFuncion();

let myFuncion = function (){
    crossOriginIsolated.log("Saludos desde la anonima");
}

let miFuncionFlecha = () => {
    console.log("Saludos desde mi funcion flecha");
}

miFuncionFlecha();

const saludar = () => console.log("Saludos a todos desde esta funsion flecha");

saludar();

const saludar2 = () => {
    return "Saludos desde la funcion flecha dos";
}

console.log(saludar2());

const saludar3 = () => "Saludos desde la funcion flecha tres";

console.log(saludar3());

const regresaObjeto = () => ({nombre: "Juan", apellido: "Lara"});

console.log(regresaObjeto()); {nombre: "juan", apellido: "lara" };

const funcionParametros = (mensaje) => console.log(mensaje);

funcionParametros("saludos desde esta funcion con parametros");

const funcionParametrosClasica = function(mensaje){
    console.log(mensaje);
}

funcionParametrosClasica("Saludos desde la funcion Clasica");

const  funcionParametros = mensaje => console.log(mensaje);

funcionParametros("Otra forma de trabajar con funcion flecha");

const funcionParametros2 = (op1, op2) => {
   let resultado = op1 + op2;
    return resultado 
}
console.log(funcionConParametros2(3,5)); 8


