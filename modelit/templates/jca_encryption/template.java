import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.util.Base64;

public class JCAEncryptionDemo {
    public static void main(String[] args) {
        try {
            String creditCardNumber = "4532 1234 5678 9010";
            System.out.println("Original Credit Card: " + creditCardNumber);

            KeyGenerator keyGen = KeyGenerator.getInstance("AES");
            keyGen.init(256);
            SecretKey secretKey = keyGen.generateKey();

            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] encryptedBytes = cipher.doFinal(creditCardNumber.getBytes());
            String encryptedData = Base64.getEncoder().encodeToString(encryptedBytes);
            
            System.out.println("Encrypted Data (Saved to DB): " + encryptedData);

            cipher.init(Cipher.DECRYPT_MODE, secretKey);
            byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(encryptedData));
            String decryptedData = new String(decryptedBytes);
            
            System.out.println("Decrypted Data (For UI display): " + decryptedData);

        } catch (Exception e) {
            System.err.println("Cryptography Error: " + e.getMessage());
        }
    }
}