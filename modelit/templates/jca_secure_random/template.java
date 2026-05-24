import java.security.SecureRandom;

public class SecureRandomOTPDemo {
    public static void main(String[] args) {
        SecureRandom secureRandom = new SecureRandom();
        
        int otp = 100000 + secureRandom.nextInt(900000);
        
        System.out.println("Your Bank Verification OTP is: " + otp);
        System.out.println("Do not share this with anyone.");

        byte[] sessionToken = new byte[32];
        secureRandom.nextBytes(sessionToken);
        StringBuilder hexToken = new StringBuilder();
        for (byte b : sessionToken) hexToken.append(String.format("%02x", b));
        
        System.out.println("\nGenerated Secure Session Token: " + hexToken.toString());
    }
}