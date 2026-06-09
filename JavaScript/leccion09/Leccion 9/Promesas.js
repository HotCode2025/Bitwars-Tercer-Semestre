let miPromesa = new Promise ( (resolver, rechazar) => {
    let expresion = true;
    if(expresion){
        //resolver('Resolvio correctamente');
    } else {
        //rechazar('Se produjo un error');
    }
});

//miPromesa.then(
//    valor => console.log(valor),
//    error => console.log(error)
//);

//miPromesa
//.then( valor => console.log(valor))
//.catch(error => console.log(error));

let promesa = new Promise( (Resolver) => {
    console.log('Inicio promesa');
    setTimeout( () => Resolver('Saludos desde promesa, callback, funcion flecha y setTimeout'), 3000);
    //console.log('Final promesa');
});

//El llamado a la promesa
//promesa.then( valor => console.log(valor));

//async indica que una funcion regresa una promesa
async function miFuncionPromesa() {
    return 'Saludos con promesas y asinc';
}

//miFuncionPromesa().then(valor => console.log(valor));

//async/await
async function funcionConPromesaYAwait() {
    let miPromesa = new Promise(resolver => {
        resolver('Promesa con await');
    });
    console.log(await miPromesa);
}

//funcionConPromesaYAwait();

//Promesas, await, async y setTimeout
async function funcionConPromesaAwaitTimeout() {
    let miPromesa = new Promise(resolver => {
        console.log('Inicio funcion');
        setTimeout(()=> resolver('Promesa con await y Timeout'), 3000);
        console.log('Final funcion');
    });
    console.log(await miPromesa);
}

//Llamamos a la funcion
funcionConPromesaAwaitTimeout();