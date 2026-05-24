public class Employee {
    private final String name;
    private final String department;
    private final double salary;
    private final int yearJoined;

    public Employee(String name, String department, double salary, int yearJoined) {
        this.name = name;
        this.department = department;
        this.salary = salary;
        this.yearJoined = yearJoined;
    }

    public String getName() { return name; }
    public String getDepartment() { return department; }
    public double getSalary() { return salary; }
    public int getYearJoined() { return yearJoined; }

    @Override
    public String toString() {
        return String.format("%s ($%.0f)", name, salary);
    }
}