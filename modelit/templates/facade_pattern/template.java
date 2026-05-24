class LightingSystem {
    void turnOn() { System.out.println("Lights: ON (Dimming to 50%)"); }
    void turnOff() { System.out.println("Lights: OFF"); }
}

class CoolingSystem {
    void setTemp(int temp) { System.out.println("AC: ON & Set to " + temp + "°C"); }
    void turnOff() { System.out.println("AC: OFF"); }
}

class SecuritySystem {
    void arm() { System.out.println("Security: ARMED"); }
    void disarm() { System.out.println("Security: DISARMED"); }
}

class SmartHomeFacade {
    private LightingSystem light = new LightingSystem();
    private CoolingSystem ac = new CoolingSystem();
    private SecuritySystem security = new SecuritySystem();

    public void arriveHome() {
        System.out.println("\n--- Entering Home Mode ---");
        security.disarm();
        light.turnOn();
        ac.setTemp(22);
    }

    public void leaveHome() {
        System.out.println("\n--- Leaving Home Mode ---");
        ac.turnOff();
        light.turnOff();
        security.arm();
    }
}

public class FacadeDemo {
    public static void main(String[] args) {
        SmartHomeFacade homeApp = new SmartHomeFacade();
        homeApp.arriveHome();
        homeApp.leaveHome();
    }
}