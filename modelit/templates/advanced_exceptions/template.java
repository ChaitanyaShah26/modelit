import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

class InsufficientFundsException extends Exception {
    public InsufficientFundsException(String message) {
        super(message);
    }
}

public class AdvancedExceptionDemo {
    
    public static void processTransfer(int accountBalance, int transferAmount) throws InsufficientFundsException {
        if (transferAmount > accountBalance) {
            throw new InsufficientFundsException("Transfer failed: Attempted to send $" + transferAmount + " but balance is $" + accountBalance);
        }
        System.out.println("Transfer of $" + transferAmount + " completed successfully.");
    }

    public static void main(String[] args) {
        try {
            processTransfer(5000, 7500);
        } catch (InsufficientFundsException e) {
            System.err.println("Business Error: " + e.getMessage());
        }

        System.out.println("-----------------");

        String filePath = "non_existent_transactions.csv";
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            System.out.println(reader.readLine());
            int value = Integer.parseInt("Not_A_Number"); 
            
        } catch (IOException | NumberFormatException e) {
            System.err.println("System Failure: Could not process file or format was corrupted.");
            System.err.println("Root Cause: " + e.getClass().getSimpleName() + " -> " + e.getMessage());
        } finally {
            System.out.println("Cleanup executed. System remains stable.");
        }
    }
}