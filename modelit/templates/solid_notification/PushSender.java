public class PushSender implements NotificationSender {
    @Override
    public void send(String message, String recipient) {
        System.out.println("[PUSH] Sending to device " + recipient + " -> " + message);
    }
}