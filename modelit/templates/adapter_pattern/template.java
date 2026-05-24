interface PaymentProcessor {
    void processPayment(double amount);
}

class StripeService {
    public void makePayment(double amountInCents) {
        System.out.println("Stripe: Processing payment of " + amountInCents + " cents successfully.");
    }
}

class StripeAdapter implements PaymentProcessor {
    private StripeService stripeService = new StripeService();

    public void processPayment(double amount) {
        double amountInCents = amount * 100;
        stripeService.makePayment(amountInCents);
    }
}

public class AdapterDemo {
    public static void main(String[] args) {
        PaymentProcessor processor = new StripeAdapter();
        processor.processPayment(50.00); 
    }
}