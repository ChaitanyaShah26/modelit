public class EmailSender implements NotificationSender {
    @Override
    public void send(String message, String recipient) {
        System.out.println("[EMAIL] Sending to " + recipient + " -> " + message);
    }
}