interface Button { void render(); }
interface Checkbox { void render(); }

class WinButton implements Button {
    public void render() { System.out.println("Rendering Windows Button"); }
}
class MacButton implements Button {
    public void render() { System.out.println("Rendering macOS Button"); }
}

class WinCheckbox implements Checkbox {
    public void render() { System.out.println("Rendering Windows Checkbox"); }
}
class MacCheckbox implements Checkbox {
    public void render() { System.out.println("Rendering macOS Checkbox"); }
}

interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

class WindowsFactory implements GUIFactory {
    public Button createButton() { return new WinButton(); }
    public Checkbox createCheckbox() { return new WinCheckbox(); }
}

class MacOSFactory implements GUIFactory {
    public Button createButton() { return new MacButton(); }
    public Checkbox createCheckbox() { return new MacCheckbox(); }
}

public class AbstractFactoryDemo {
    public static void main(String[] args) {
        String os = "Mac"; 
        GUIFactory factory = os.equals("Mac") ? new MacOSFactory() : new WindowsFactory();
        
        Button button = factory.createButton();
        Checkbox checkbox = factory.createCheckbox();
        
        button.render();
        checkbox.render();
    }
}