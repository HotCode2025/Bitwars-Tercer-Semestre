mifuncion1()
mifuncion2()


function mifuncion(){
    console.log("Funcion"); "Funcion 1"

}

function mifuncion2(){
    console.log("Funcion 2"); "Funcion 2"
}

let imp = function imprimir(mensaje){
    console.log(mensaje);
}

function sumar(op1, op2, funcionCallback){
    let res = op1 + op2;
    funcionCallback("Resultado: ${res}");
}

sumar(5,3,imprimir);

function miFuncionCallback(){
    console.log("Saludo asinconico despues de 3 segundos");
}

setTimeout(miFuncionCallback, 3000);

setTimeout(function(){console.log("saludo asinconico 2")}, 4000);

setTimeout( () => console.log("Saludo Asinconico 3"), 5000);

let reloj = () => {
    let fecha = new Date();
    console.log(`${fecha.getHours()}:${fecha.getMinutes()}:${fecha.getSeconds()}`);
}

setInterval(reloj, 1000); 