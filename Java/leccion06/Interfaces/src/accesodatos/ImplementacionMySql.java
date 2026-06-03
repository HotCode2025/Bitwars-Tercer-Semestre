package accesodatos;

public class ImplementacionMySql implements IAccesoDatos{
    
    @Override
    public void insertar() {
        System.out.println("Insertar desde My");
    }
    
    @Override
    public void listar() {
        System.out.println("desde MySql");
    }
    
    @Override
    public void actualizar() {
        System.out.println("Insertar desde MySql");
    }
    @Override
    public void eliminar() {
        System.out.println("Insertar desde MySQl");
    }
    
}