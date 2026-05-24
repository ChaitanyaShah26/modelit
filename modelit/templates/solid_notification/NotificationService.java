public class NotificationService {
    private final NotificationSender sender;

    public NotificationService(NotificationSender sender) {
        this.sender = sender;
    }

    public void alert(String message, String recipient) {
        sender.send(message, recipient);
    }
}