class ResourceLock {
    public static final Object INVENTORY = new Object();
    public static final Object LOGISTICS = new Object();
}

class FlawedProducer extends Thread {
    public void run() {
        synchronized (ResourceLock.INVENTORY) {
            System.out.println("Producer locked INVENTORY. Processing items...");
            try { Thread.sleep(50); } catch (Exception e) {} 
            
            System.out.println("Producer waiting to lock LOGISTICS...");
            synchronized (ResourceLock.LOGISTICS) {
                System.out.println("Producer successfully sent items to logistics.");
            }
        }
    }
}

class FlawedConsumer extends Thread {
    public void run() {
        synchronized (ResourceLock.LOGISTICS) {
            System.out.println("Consumer locked LOGISTICS. Preparing trucks...");
            try { Thread.sleep(50); } catch (Exception e) {} 
            
            System.out.println("Consumer waiting to lock INVENTORY...");
            synchronized (ResourceLock.INVENTORY) {
                System.out.println("Consumer successfully retrieved items from inventory.");
            }
        }
    }
}

public class DeadlockDemo {
    public static void main(String[] args) {
        System.out.println("Starting flawed system. (Program will hang/deadlock)");
        new FlawedProducer().start();
        new FlawedConsumer().start();
    }
}