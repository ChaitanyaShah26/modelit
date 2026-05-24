interface Visitor {
    double visit(Grocery grocery);
    double visit(Electronics electronics);
}

interface CartItem {
    double accept(Visitor visitor);
}

class Grocery implements CartItem {
    private double price;
    public Grocery(double price) { this.price = price; }
    public double getPrice() { return price; }
    public double accept(Visitor visitor) { return visitor.visit(this); }
}

class Electronics implements CartItem {
    private double price;
    public Electronics(double price) { this.price = price; }
    public double getPrice() { return price; }
    public double accept(Visitor visitor) { return visitor.visit(this); }
}

class TaxVisitor implements Visitor {
    public double visit(Grocery grocery) {
        return grocery.getPrice() * 0.05; 
    }
    public double visit(Electronics electronics) {
        return electronics.getPrice() * 0.18; 
    }
}

public class VisitorDemo {
    public static void main(String[] args) {
        CartItem apple = new Grocery(100);
        CartItem laptop = new Electronics(50000);
        TaxVisitor taxCalculator = new TaxVisitor();

        System.out.println("Tax on Apple (Grocery): $" + apple.accept(taxCalculator));
        System.out.println("Tax on Laptop (Electronics): $" + laptop.accept(taxCalculator));
    }
}