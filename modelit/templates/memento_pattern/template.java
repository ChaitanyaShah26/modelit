class GameSave {
    private final int level;
    private final int health;

    public GameSave(int level, int health) {
        this.level = level;
        this.health = health;
    }
    public int getLevel() { return level; }
    public int getHealth() { return health; }
}

class Player {
    private int level = 1;
    private int health = 100;

    public void takeDamage(int damage) { health -= damage; }
    public void levelUp() { level++; }

    public GameSave save() {
        System.out.println(">> Game Saved. Level: " + level + ", Health: " + health);
        return new GameSave(level, health);
    }

    public void restore(GameSave save) {
        this.level = save.getLevel();
        this.health = save.getHealth();
        System.out.println(">> Game Restored. Level: " + level + ", Health: " + health);
    }

    public void status() { System.out.println("Current Status -> Level: " + level + ", Health: " + health); }
}

public class MementoDemo {
    public static void main(String[] args) {
        Player player = new Player();
        player.status();

        player.levelUp();
        player.takeDamage(20);
        
        GameSave checkpoint = player.save();

        player.takeDamage(80);
        player.status();

        player.restore(checkpoint);
        player.status();
    }
}