interface OrderState {
    void next(Order order);
    void printStatus();
}

class PlacedState implements OrderState {
    public void next(Order order) { order.setState(new ShippedState()); }
    public void printStatus() { System.out.println("State: Order has been PLACED."); }
}

class ShippedState implements OrderState {
    public void next(Order order) { order.setState(new DeliveredState()); }
    public void printStatus() { System.out.println("State: Order has been SHIPPED."); }
}

class DeliveredState implements OrderState {
    public void next(Order order) { System.out.println("Order is already delivered."); }
    public void printStatus() { System.out.println("State: Order is DELIVERED."); }
}

class Order {
    private OrderState state = new PlacedState();

    public void setState(OrderState state) { this.state = state; }
    public void nextState() { state.next(this); }
    public void checkStatus() { state.printStatus(); }
}

public class StateDemo {
    public static void main(String[] args) {
        Order myOrder = new Order();
        myOrder.checkStatus();

        myOrder.nextState();
        myOrder.checkStatus();

        myOrder.nextState();
        myOrder.checkStatus();
    }
}