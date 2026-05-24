public class SlackSender implements NotificationSender {
    @Override
    public void send(String message, String recipient) {
        System.out.println("[SLACK] Sending to channel " + recipient + " -> " + message);
    }
}