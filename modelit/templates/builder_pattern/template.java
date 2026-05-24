class UserProfile {
    private final String username; 
    private final String email;    
    private final int age;         
    private final String phone;    

    private UserProfile(Builder builder) {
        this.username = builder.username;
        this.email = builder.email;
        this.age = builder.age;
        this.phone = builder.phone;
    }

    public void showProfile() {
        System.out.println("User: " + username + " | Email: " + email + " | Age: " + age + " | Phone: " + phone);
    }

    static class Builder {
        private String username;
        private String email;
        private int age = 0; 
        private String phone = "N/A";

        public Builder(String username, String email) {
            this.username = username;
            this.email = email;
        }

        public Builder setAge(int age) {
            this.age = age;
            return this;
        }

        public Builder setPhone(String phone) {
            this.phone = phone;
            return this;
        }

        public UserProfile build() {
            return new UserProfile(this);
        }
    }
}

public class BuilderDemo {
    public static void main(String[] args) {
        UserProfile user1 = new UserProfile.Builder("user", "user@example.com")
                                           .setAge(21)
                                           .build();
        
        UserProfile user2 = new UserProfile.Builder("admin_user", "admin@sys.com")
                                           .setPhone("+91-9876543210")
                                           .build();

        user1.showProfile();
        user2.showProfile();
    }
}