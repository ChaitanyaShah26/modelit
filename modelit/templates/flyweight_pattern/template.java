import java.util.HashMap;

class TreeType {
    private String name;
    private String color;
    private String textureData;

    public TreeType(String name, String color, String textureData) {
        this.name = name;
        this.color = color;
        this.textureData = textureData;
    }

    public void draw(int x, int y) {
        System.out.println("Drawing a " + color + " " + name + " tree at X:" + x + ", Y:" + y);
    }
}

class TreeFactory {
    private static HashMap<String, TreeType> treeTypes = new HashMap<>();

    public static TreeType getTreeType(String name, String color, String textureData) {
        String key = name + "_" + color;
        if (!treeTypes.containsKey(key)) {
            treeTypes.put(key, new TreeType(name, color, textureData));
            System.out.println("--> CACHE MISS: Instantiated new TreeType: " + key);
        }
        return treeTypes.get(key);
    }
}

public class FlyweightDemo {
    public static void main(String[] args) {
        System.out.println("Planting Forest...\n");
        
        TreeType oak = TreeFactory.getTreeType("Oak", "Green", "Oak_Texture.png");
        oak.draw(10, 20);
        
        TreeType oak2 = TreeFactory.getTreeType("Oak", "Green", "Oak_Texture.png");
        oak2.draw(50, 60);

        TreeType pine = TreeFactory.getTreeType("Pine", "Dark-Green", "Pine_Texture.png");
        pine.draw(100, 100);
        
        System.out.println("\nTotal unique tree types in memory: 2 (Even if we plant 10,000 trees)");
    }
}