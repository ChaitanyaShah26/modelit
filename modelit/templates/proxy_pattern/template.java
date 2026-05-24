interface DatabaseExecutor {
    void executeQuery(String query) throws Exception;
}

class RealDatabaseExecutor implements DatabaseExecutor {
    public void executeQuery(String query) {
        System.out.println("Executing Query: " + query);
    }
}

class ProxyDatabaseExecutor implements DatabaseExecutor {
    private boolean isAdmin;
    private RealDatabaseExecutor realExecutor;

    public ProxyDatabaseExecutor(String userRole) {
        this.isAdmin = "ADMIN".equalsIgnoreCase(userRole);
        this.realExecutor = new RealDatabaseExecutor();
    }

    public void executeQuery(String query) throws Exception {
        if (!isAdmin && (query.toUpperCase().startsWith("DROP") || query.toUpperCase().startsWith("DELETE"))) {
            throw new Exception("Access Denied: Only Admins can execute destructive queries.");
        }
        realExecutor.executeQuery(query);
    }
}

public class ProxyDemo {
    public static void main(String[] args) {
        DatabaseExecutor nonAdminExecutor = new ProxyDatabaseExecutor("USER");
        DatabaseExecutor adminExecutor = new ProxyDatabaseExecutor("ADMIN");

        try {
            nonAdminExecutor.executeQuery("SELECT * FROM users");
            System.out.println("Select query successful by USER.");
            nonAdminExecutor.executeQuery("DELETE FROM users"); 
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }

        try {
            adminExecutor.executeQuery("DELETE FROM users");
            System.out.println("Delete query successful by ADMIN.");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}