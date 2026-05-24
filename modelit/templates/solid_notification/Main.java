import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        String alertMessage = "Server is down!";
        String adminContact = "admin_team";

        NotificationService emailService = new NotificationService(new EmailSender());
        NotificationService smsService   = new NotificationService(new SmsSender());
        NotificationService pushService  = new NotificationService(new PushSender());
        NotificationService slackService = new NotificationService(new SlackSender());

        List<NotificationService> activeServices = Arrays.asList(
                emailService, smsService, pushService, slackService
        );

        System.out.println("--- INITIATING EMERGENCY BROADCAST ---");
        
        for (NotificationService service : activeServices) {
            service.alert(alertMessage, adminContact);
        }
    }
}