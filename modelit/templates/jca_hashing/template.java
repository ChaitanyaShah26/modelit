import java.security.MessageDigest;

public class HashingDemo {
    public static String hashPassword(String plainTextPassword) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashedBytes = md.digest(plainTextPassword.getBytes());
            
            StringBuilder hexString = new StringBuilder();
            for (byte b : hashedBytes) {
                hexString.append(String.format("%02x", b));
            }
            return hexString.toString();
        } catch (Exception e) {
            throw new RuntimeException("Error generating hash", e);
        }
    }

    public static void main(String[] args) {
        String userPassword = "MySecurePassword123!";
        String dbHash = hashPassword(userPassword);
        
        System.out.println("Original Password: " + userPassword);
        System.out.println("SHA-256 Hash (Stored in DB): " + dbHash);
    }
}