interface Device {
    void turnOn();
    void turnOff();
    void setVolume(int percent);
}

class SmartTV implements Device {
    private int volume = 30;
    public void turnOn() { System.out.println("Smart TV is ON"); }
    public void turnOff() { System.out.println("Smart TV is OFF"); }
    public void setVolume(int percent) { 
        volume = percent; 
        System.out.println("Smart TV Volume set to " + volume); 
    }
}

abstract class RemoteControl {
    protected Device device;
    public RemoteControl(Device device) { this.device = device; }
    public abstract void togglePower();
}

class BasicRemote extends RemoteControl {
    public BasicRemote(Device device) { super(device); }
    public void togglePower() {
        System.out.println("\n[Basic Remote Used]");
        device.turnOn();
    }
}

class AdvancedRemote extends RemoteControl {
    public AdvancedRemote(Device device) { super(device); }
    public void togglePower() {
        System.out.println("\n[Advanced Remote Used]");
        device.turnOn();
    }
    public void mute() {
        System.out.println("Muting Device...");
        device.setVolume(0);
    }
}

public class BridgeDemo {
    public static void main(String[] args) {
        Device tv = new SmartTV();
        
        BasicRemote basicRemote = new BasicRemote(tv);
        basicRemote.togglePower();
        
        AdvancedRemote advancedRemote = new AdvancedRemote(tv);
        advancedRemote.togglePower();
        advancedRemote.mute();
    }
}