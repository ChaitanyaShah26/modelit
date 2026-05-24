interface ConfigPrototype {
    ConfigPrototype clone();
}

class DatabaseConfig implements ConfigPrototype {
    private String host;
    private int port;
    private String dbName;

    public DatabaseConfig(String host, int port, String dbName) {
        System.out.println("Connecting to Database server... (Expensive Operation)");
        this.host = host;
        this.port = port;
        this.dbName = dbName;
    }

    public void setDbName(String dbName) { this.dbName = dbName; }

    @Override
    public ConfigPrototype clone() {
        return new DatabaseConfig(this.host, this.port, this.dbName);
    }

    public void showConfig() {
        System.out.println("DB Config [Host: " + host + ", Port: " + port + ", DB: " + dbName + "]");
    }
}

public class PrototypeDemo {
    public static void main(String[] args) {
        DatabaseConfig devConfig = new DatabaseConfig("localhost", 5432, "dev_db");
        devConfig.showConfig();

        DatabaseConfig prodConfig = (DatabaseConfig) devConfig.clone();
        prodConfig.setDbName("prod_db");
        prodConfig.showConfig();
    }
}