import java.util.ArrayList;
import java.util.List;

interface FileSystemComponent {
    void showDetails();
    int getSize();
}

class File implements FileSystemComponent {
    private String name;
    private int size;

    public File(String name, int size) { this.name = name; this.size = size; }
    public void showDetails() { System.out.println("   File: " + name + " (" + size + " KB)"); }
    public int getSize() { return size; }
}

class Directory implements FileSystemComponent {
    private String name;
    private List<FileSystemComponent> components = new ArrayList<>();

    public Directory(String name) { this.name = name; }
    public void addComponent(FileSystemComponent component) { components.add(component); }

    public void showDetails() {
        System.out.println("Directory: " + name + " | Total Size: " + getSize() + " KB");
        for (FileSystemComponent component : components) {
            component.showDetails();
        }
    }

    public int getSize() {
        return components.stream().mapToInt(FileSystemComponent::getSize).sum();
    }
}

public class CompositeDemo {
    public static void main(String[] args) {
        File file1 = new File("resume.pdf", 500);
        File file2 = new File("photo.png", 1500);
        File file3 = new File("system_config.txt", 15);

        Directory personalDir = new Directory("Personal Files");
        personalDir.addComponent(file1);
        personalDir.addComponent(file2);

        Directory rootDir = new Directory("Root");
        rootDir.addComponent(personalDir);
        rootDir.addComponent(file3);

        rootDir.showDetails();
    }
}