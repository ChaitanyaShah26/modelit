interface Coffee {
    String getDescription();
    double getCost();
}

class Espresso implements Coffee {
    public String getDescription() { return "Espresso"; }
    public double getCost() { return 150.0; }
}

abstract class CoffeeDecorator implements Coffee {
    protected Coffee decoratedCoffee;
    public CoffeeDecorator(Coffee coffee) { this.decoratedCoffee = coffee; }
    public String getDescription() { return decoratedCoffee.getDescription(); }
    public double getCost() { return decoratedCoffee.getCost(); }
}

class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }
    public String getDescription() { return super.getDescription() + ", Steamed Milk"; }
    public double getCost() { return super.getCost() + 30.0; }
}

class CaramelDecorator extends CoffeeDecorator {
    public CaramelDecorator(Coffee coffee) { super(coffee); }
    public String getDescription() { return super.getDescription() + ", Caramel Syrup"; }
    public double getCost() { return super.getCost() + 45.0; }
}

public class DecoratorDemo {
    public static void main(String[] args) {
        Coffee myOrder = new Espresso();
        myOrder = new MilkDecorator(myOrder);
        myOrder = new CaramelDecorator(myOrder);

        System.out.println("Order Details: " + myOrder.getDescription());
        System.out.println("Total Cost: ₹" + myOrder.getCost());
    }
}