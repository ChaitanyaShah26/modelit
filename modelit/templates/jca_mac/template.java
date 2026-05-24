import javax.crypto.Mac;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.util.Base64;

public class MACSessionDemo {
    public static void main(String[] args) throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("HmacSHA256");
        SecretKey serverSecretKey = keyGen.generateKey();
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(serverSecretKey);

        String sessionData = "userId=105&role=user";
        byte[] macResult = mac.doFinal(sessionData.getBytes());
        String macCode = Base64.getEncoder().encodeToString(macResult);
        
        System.out.println("Cookie sent to browser: " + sessionData + "&mac=" + macCode);

        String hackedSessionData = "userId=105&role=admin"; 
        
        byte[] newMacResult = mac.doFinal(hackedSessionData.getBytes());
        String expectedMacCode = Base64.getEncoder().encodeToString(newMacResult);

        if (expectedMacCode.equals(macCode)) {
            System.out.println("Session Validated! Welcome, Admin.");
        } else {
            System.out.println("SECURITY ALERT: Session Tampering Detected! Request Rejected.");
        }
    }
}