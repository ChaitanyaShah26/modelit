import java.security.*;
import java.util.Base64;

public class DigitalSignatureDemo {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        keyGen.initialize(2048);
        KeyPair pair = keyGen.generateKeyPair();

        String firmwareData = "v1.5_Firmware_Update_Binary_Code";

        Signature signatureAlgorithm = Signature.getInstance("SHA256withRSA");
        signatureAlgorithm.initSign(pair.getPrivate());
        signatureAlgorithm.update(firmwareData.getBytes());
        
        byte[] digitalSignature = signatureAlgorithm.sign();
        String signatureString = Base64.getEncoder().encodeToString(digitalSignature);
        System.out.println("Firmware signed by Manufacturer. Signature: " + signatureString.substring(0, 30) + "...");

        Signature verificationAlgorithm = Signature.getInstance("SHA256withRSA");
        verificationAlgorithm.initVerify(pair.getPublic());
        verificationAlgorithm.update(firmwareData.getBytes()); 

        boolean isAuthentic = verificationAlgorithm.verify(digitalSignature);

        if (isAuthentic) {
            System.out.println("Device: Firmware is AUTHENTIC. Proceeding with installation.");
        } else {
            System.out.println("Device: FIRMWARE TAMPERED! Installation aborted.");
        }
    }
}