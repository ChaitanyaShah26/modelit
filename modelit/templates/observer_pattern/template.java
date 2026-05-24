import java.util.ArrayList;
import java.util.List;

interface Observer {
    void update(String stockName, double price);
}

class Investor implements Observer {
    private String name;
    public Investor(String name) { this.name = name; }
    public void update(String stockName, double price) {
        System.out.println("Notification for " + name + ": " + stockName + " is now $" + price);
    }
}

class StockMarket {
    private List<Observer> investors = new ArrayList<>();
    private String stockName;
    private double price;

    public StockMarket(String stockName) { this.stockName = stockName; }

    public void subscribe(Observer investor) { investors.add(investor); }

    public void updatePrice(double newPrice) {
        this.price = newPrice;
        System.out.println("\n[MARKET UPDATE] " + stockName + " changed to $" + newPrice);
        for (Observer investor : investors) {
            investor.update(stockName, price);
        }
    }
}

public class ObserverDemo {
    public static void main(String[] args) {
        StockMarket reliance = new StockMarket("Reliance Industries");

        Investor investor1 = new Investor("Rahul");
        Investor investor2 = new Investor("Neha");

        reliance.subscribe(investor1);
        reliance.subscribe(investor2);

        reliance.updatePrice(2500.50);
        reliance.updatePrice(2512.00);
    }
}