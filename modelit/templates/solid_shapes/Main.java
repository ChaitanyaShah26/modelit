import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Shape> mixedShapes = Arrays.asList(
            new Circle(5.0),                  
            new Rectangle(4.0, 6.0),          
            new Triangle(3.0, 8.0),           
            new Pentagon(4.0, 2.75)           
        );

        AreaCalculator calculator = new AreaCalculator();
        double total = calculator.calculateTotalArea(mixedShapes);
        
        System.out.println("--- SHAPE AREA CALCULATOR ---");
        System.out.println("Processing " + mixedShapes.size() + " different shapes...");
        System.out.printf("Total Combined Area: %.2f sq units\n", total);
    }
}