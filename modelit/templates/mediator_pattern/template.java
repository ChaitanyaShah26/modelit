import java.util.ArrayList;
import java.util.List;

interface ATCMediator {
    void registerFlight(Flight flight);
    boolean requestLanding(Flight flight);
}

class ControlTower implements ATCMediator {
    private List<Flight> flights = new ArrayList<>();
    private boolean runwayAvailable = true;

    public void registerFlight(Flight flight) { flights.add(flight); }

    public boolean requestLanding(Flight flight) {
        if (runwayAvailable) {
            System.out.println("ATC: Runway cleared for " + flight.getName());
            runwayAvailable = false;
            return true;
        } else {
            System.out.println("ATC: Runway busy! " + flight.getName() + " must hold.");
            return false;
        }
    }

    public void clearRunway() {
        System.out.println("ATC: Runway is now clear.");
        runwayAvailable = true;
    }
}

class Flight {
    private String name;
    private ATCMediator atc;

    public Flight(String name, ATCMediator atc) {
        this.name = name;
        this.atc = atc;
        atc.registerFlight(this);
    }
    public String getName() { return name; }
    
    public void land() {
        if (atc.requestLanding(this)) {
            System.out.println(name + ": Landing successful.");
            ((ControlTower) atc).clearRunway(); 
        } else {
            System.out.println(name + ": Waiting for clearance...");
        }
    }
}

public class MediatorDemo {
    public static void main(String[] args) {
        ControlTower atc = new ControlTower();
        Flight f1 = new Flight("Boeing 747", atc);
        Flight f2 = new Flight("Airbus A320", atc);

        f1.land();
        f2.land(); 
    }
}