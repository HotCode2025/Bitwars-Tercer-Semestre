import java.util.Scanner;

public class CalculadoraUTN {

    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in); 

        while (true) {
            System.out.println("******* Aplicacion Calculadora *******");
            mostrarMenu();

            try {
                var operacion = Integer.parseInt(entrada.nextLine());

                if (operacion >= 1 && operacion <= 4) {
                    ejecutarOperacion(operacion, entrada); 
                } else if (operacion == 5) {
                    System.out.println("Hasta pronto...");
                    break;
                } else {
                    System.out.println("Opcion erronea.");
                    System.out.println();
                }
            } catch (Exception e) {
                System.out.println("Ocurrio un error: " + e.getMessage()); 
        } // Fin While
    } // Fin main

    private static void mostrarMenu() {
        System.out.println("""
                1. Suma
                2. Resta
                3. Multiplicacion
                4. Division
                5. Salir
                """);
        System.out.println("Operacion a realizar?");
    }

    private static void ejecutarOperacion(int operacion, Scanner entrada) { 
        System.out.print("Digite el valor para el operando1: ");
        var operando1 = Double.parseDouble(entrada.nextLine());
        System.out.print("Digite el valor para el operando2: ");
        var operando2 = Double.parseDouble(entrada.nextLine());

        double resultado;

        switch (operacion) {
            case 1 -> { 
                resultado = operando1 + operando2; 
                System.out.println("Resultado de la suma: " + resultado); 
            }
            case 2 -> {
                resultado = operando1 - operando2;
                System.out.println("Resultado de la resta: " + resultado);
            }
            case 3 -> {
                if (operando2 == 0) {
                    System.out.println("Error: no se puede dividir por cero.");
                } else {
                    resultado = operando1 / operando2;
                    System.out.println("Resultado de la division: " + resultado);
                }
            }
            case 4 -> {
                resultado = operando1 * operando2;
                System.out.println("Resultado de la multiplicacion: " + resultado);
            }
            default -> System.out.println("Operacion erronea: " + operacion);
        }
    }
}
