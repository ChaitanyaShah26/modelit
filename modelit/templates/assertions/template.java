class DiscountCalculator {
    public static double applyDiscount(double originalPrice, double discountPercentage) {
        double discountAmount = originalPrice * (discountPercentage / 100);
        double finalPrice = originalPrice - discountAmount;
        
        assert finalPrice >= 0 : "CRITICAL LOGIC ERROR: Final price fell below zero!";
        
        return finalPrice;
    }
}

public class AssertionDemo {
    public static void main(String[] args) {
        System.out.println("Final Price: $" + DiscountCalculator.applyDiscount(1000, 20));
        
        System.out.println("Testing invalid logic...");
        System.out.println("Final Price: $" + DiscountCalculator.applyDiscount(500, 150)); 
    }
}