import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class HMACWebhookDemo {
    private static final String SHARED_SECRET = "super_secret_api_key_123";
    private static final String HMAC_ALGO = "HmacSHA256";

    public static String generateHMAC(String payload) throws Exception {
        Mac mac = Mac.getInstance(HMAC_ALGO);
        SecretKeySpec secretKey = new SecretKeySpec(SHARED_SECRET.getBytes(), HMAC_ALGO);
        mac.init(secretKey);
        
        byte[] hmacBytes = mac.doFinal(payload.getBytes());
        return Base64.getEncoder().encodeToString(hmacBytes);
    }

    public static void main(String[] args) throws Exception {
        String jsonPayload = "{\"payment_status\": \"success\", \"amount\": 5000}";
        String incomingSignature = generateHMAC(jsonPayload); 
        System.out.println("Incoming Webhook Signature: " + incomingSignature);

        String expectedSignature = generateHMAC(jsonPayload);
        
        if (expectedSignature.equals(incomingSignature)) {
            System.out.println("Verification SUCCESS: Payload is authentic.");
        } else {
            System.out.println("Verification FAILED: Payload was tampered with!");
        }
    }
}