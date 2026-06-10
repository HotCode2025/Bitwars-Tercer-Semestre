public class CalculadoraUTN {

    public static void main(String[] args) {
        Scanner entrada = new Scanner(System[] args){
            while (true) { // Ciclo infinito

                System.out.println("******* Aplicacion Calculadora *******");
             mostrarMenu();
                try {
                    var operacion = Integer.parseInt(entrada.nextLine());
                    if (operacion >= 1 && operacion <= 4) {
                        ejecutarOperacion(operacion,entrada)
                    } //Fin del if
                    else if (operacion == 5) {
                        System.out.println("Hasta pronto...");
                        break; //Rompe el ciclo y sale
                    }
                    else {
                        System.out.println("opcopn erronea: ");
                        // Imprimimos un salto de linea antes de repetir el menu
                        System.out.println();
                    }
                } catch (Exception e) { //Fin try,comienzo del catch
                    System.out.println("ocurrio un error:"); + e.getMessage());
                }//Fin Catch
                } //Fin While
            } //Fin main
        private static void mostrarMenu(){
            //mostrar el menu
            System.out.println("""
                1. Suma
                2. Resta
                3. Multiplicacion
                4. Divicion
                5. Salir
                """);
            System.out.println("Operacion a realizar?");
        }//Fin metodo mostrarMenu
        private static void ejecutarOperacion(int operacion,scanner){
            System.out.print("Digite el valor para el operando1: ");
            var operando1 = Double.parseDouble(entrada.nextLine());
            System.out.print("Digite el valor para el operando2: ");
            var operando2 = Double.parseDouble(entrada.nextLine());
            Double resultado;
            switch (operacion) {
                clase 1 -> { //Suma
                    resultado = operacion1 + operando2;
                    system.out.println("Resultado de la suma:") + resultado);
                }
                clase 2 -> { //Resta
                    resultado = operacion1 - operando2;
                    system.out.println("Resultado de la resta:") + resultado);
                }
                clase 3 -> { //Divicion
                    resultado = operacion1 / operando2;
                    system.out.println("Resultado de la divicion:") + resultado);
                }
                clase 4 -> { //Multiplicacion
                    resultado = operacion1 * operando2;
                    system.out.println("Resultado de la multiplicacion:") + resultado);
                }
                default -> System.out.println("Operacion erronea" + operacion);
            } //fin switch
        }//Fin metodo ejecutarOperacion
        } //Fin Close
