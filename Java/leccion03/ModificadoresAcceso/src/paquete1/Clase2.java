package paquete1;

class Clase2 extends Clase1{
    String atributoDefault = "Valor del atributo default";

    Clase2() {
        System.out.println("Constructor Default");
    }

    public Clase2(String arg) {
        super();
        this.atributoDefault = "Modificacion atributo default";
        System.out.println("atributoDefault = " + this.atributoDefault);
        this.metodoDefault();
    }

    void metodoDefault() {
        System.out.println("Método Default");
    }
}