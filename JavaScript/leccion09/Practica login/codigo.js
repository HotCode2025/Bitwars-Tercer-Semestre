// TAREA FINAL:
// Agregamos una actividad de JavaScript para el login.
// El formulario valida si los campos están completos
// y comprueba un usuario y contraseña de prueba.

let formulario = document.getElementById("loginForm");
let usuario = document.getElementById("usuario");
let password = document.getElementById("password");
let mensaje = document.getElementById("mensaje");

formulario.addEventListener("submit", function(evento){
  evento.preventDefault();

  if(usuario.value === "" || password.value === ""){
    mensaje.innerHTML = "Debes completar todos los campos";
  } else if(usuario.value === "admin" && password.value === "1234"){
    mensaje.innerHTML = "Login correcto";
  } else {
    mensaje.innerHTML = "Usuario o contraseña incorrectos";
  }
});