interface PaymentGateway {
    void processPayment(double amount);

    default void logTransaction(double amount) {
        System.out.println("[LOG] Transaction of $" + amount + " recorded in database.");
    }
}

class PayPalIntegration implements PaymentGateway {
    public void processPayment(double amount) {
        System.out.println("Processing $" + amount + " via PayPal.");
    }
}

class StripeIntegration implements PaymentGateway {
    public void processPayment(double amount) {
        System.out.println("Processing $" + amount + " via Stripe.");
    }
    
    @Override
    public void logTransaction(double amount) {
        System.out.println("[STRIPE-LOG] Advanced logging for transaction: $" + amount);
    }
}

public class DefaultMethodDemo {
    public static void main(String[] args) {
        PaymentGateway paypal = new PayPalIntegration();
        paypal.processPayment(1500.00);
        paypal.logTransaction(1500.00); 

        System.out.println("-----------------");

        PaymentGateway stripe = new StripeIntegration();
        stripe.processPayment(2500.00);
        stripe.logTransaction(2500.00);
    }
}