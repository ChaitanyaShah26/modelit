import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.util.Base64;

public class RSAKeyGenDemo {
    public static void main(String[] args) {
        try {
            System.out.println("Generating 2048-bit RSA Key Pair... Please wait.");
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
            keyGen.initialize(2048);
            
            KeyPair keyPair = keyGen.generateKeyPair();
            PublicKey publicKey = keyPair.getPublic();
            PrivateKey privateKey = keyPair.getPrivate();

            String pubKeyB64 = Base64.getEncoder().encodeToString(publicKey.getEncoded());
            String privKeyB64 = Base64.getEncoder().encodeToString(privateKey.getEncoded());

            System.out.println("\n--- PUBLIC KEY (Shareable) ---");
            System.out.println(pubKeyB64);
            
            System.out.println("\n--- PRIVATE KEY (Keep Secret!) ---");
            System.out.println(privKeyB64.substring(0, 50) + "... [REDACTED FOR SECURITY]");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}