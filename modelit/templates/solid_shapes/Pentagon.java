public class Pentagon implements Shape {
    private final double side;
    private final double apothem;

    public Pentagon(double side, double apothem) {
        this.side = side;
        this.apothem = apothem;
    }

    @Override
    public double area() {
        return 2.5 * side * apothem;
    }
}