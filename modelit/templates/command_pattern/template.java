import java.util.Stack;

class BankAccount {
    private int balance = 1000;
    public void deposit(int amount) {
        balance += amount;
        System.out.println("Deposited $" + amount + ". Current Balance: $" + balance);
    }
    public void withdraw(int amount) {
        balance -= amount;
        System.out.println("Withdrew $" + amount + ". Current Balance: $" + balance);
    }
}

interface TransactionCommand {
    void execute();
    void undo();
}

class DepositCommand implements TransactionCommand {
    private BankAccount account;
    private int amount;
    
    public DepositCommand(BankAccount account, int amount) {
        this.account = account;
        this.amount = amount;
    }
    public void execute() { account.deposit(amount); }
    public void undo() { account.withdraw(amount); }
}

class TransactionManager {
    private Stack<TransactionCommand> history = new Stack<>();

    public void executeTransaction(TransactionCommand command) {
        command.execute();
        history.push(command);
    }
    public void undoLastTransaction() {
        if (!history.isEmpty()) {
            System.out.print("Undoing last transaction... ");
            TransactionCommand lastCommand = history.pop();
            lastCommand.undo();
        }
    }
}

public class CommandDemo {
    public static void main(String[] args) {
        BankAccount myAccount = new BankAccount();
        TransactionManager manager = new TransactionManager();

        manager.executeTransaction(new DepositCommand(myAccount, 500));
        manager.executeTransaction(new DepositCommand(myAccount, 200));
        
        manager.undoLastTransaction(); 
    }
}