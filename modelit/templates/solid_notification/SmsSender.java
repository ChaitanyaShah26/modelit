public class SmsSender implements NotificationSender {
    @Override
    public void send(String message, String recipient) {
        System.out.println("[SMS] Sending to " + recipient + " -> " + message);
    }
}