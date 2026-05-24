import java.util.LinkedList;
import java.util.Queue;

class OrderQueue {
    private Queue<Integer> queue = new LinkedList<>();
    private final int MAX_CAPACITY = 3;

    public synchronized void produceOrder(int orderId) throws InterruptedException {
        while (queue.size() == MAX_CAPACITY) {
            System.out.println("Queue is FULL. Producer is waiting...");
            wait();
        }
        queue.add(orderId);
        System.out.println("Produced Order #" + orderId);
        notifyAll(); 
    }

    public synchronized void consumeOrder() throws InterruptedException {
        while (queue.isEmpty()) {
            System.out.println("Queue is EMPTY. Consumer is waiting...");
            wait();
        }
        int orderId = queue.poll();
        System.out.println("Consumed Order #" + orderId);
        notifyAll();
    }
}

public class WaitNotifyDemo {
    public static void main(String[] args) {
        OrderQueue sharedQueue = new OrderQueue();

        Thread producer = new Thread(() -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    sharedQueue.produceOrder(i);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {}
        });

        Thread consumer = new Thread(() -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    sharedQueue.consumeOrder();
                    Thread.sleep(500); 
                }
            } catch (InterruptedException e) {}
        });

        producer.start();
        consumer.start();
    }
}