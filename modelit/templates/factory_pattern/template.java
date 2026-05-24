interface Notification {
    void notifyUser();
}

class SMSNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending SMS Notification...");
    }
}

class EmailNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending Email Notification...");
    }
}

class NotificationFactory {
    public Notification createNotification(String channel) {
        if (channel == null || channel.isEmpty()) return null;
        if (channel.equalsIgnoreCase("SMS")) return new SMSNotification();
        if (channel.equalsIgnoreCase("EMAIL")) return new EmailNotification();
        return null;
    }
}

public class FactoryPatternDemo {
    public static void main(String[] args) {
        NotificationFactory factory = new NotificationFactory();
        
        Notification email = factory.createNotification("EMAIL");
        email.notifyUser();
        
        Notification sms = factory.createNotification("SMS");
        sms.notifyUser();
    }
}