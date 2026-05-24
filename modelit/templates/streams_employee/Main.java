import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        List<Employee> employees = Arrays.asList(
            new Employee("Alice", "Engineering", 95000, 2018),
            new Employee("Bob",   "Marketing",   60000, 2021),
            new Employee("Carol", "Engineering", 112000, 2020),
            new Employee("Dave",  "HR",          52000, 2019),
            new Employee("Eve",   "Marketing",   78000, 2022),
            new Employee("Frank", "Engineering", 88000, 2021)
        );

        System.out.println("--- EMPLOYEE REPORT GENERATOR ---\n");

        Map<String, Double> avgSalaryPerDept = employees.stream()
            .collect(Collectors.groupingBy(
                Employee::getDepartment, 
                Collectors.averagingDouble(Employee::getSalary)
            ));

        System.out.println("1. Average Salary per Department:");
        avgSalaryPerDept.forEach((dept, avgSal) -> 
            System.out.printf("   - %s: $%.2f\n", dept, avgSal)
        );
        System.out.println();

        Map<String, Employee> topPaidPerDept = employees.stream()
            .collect(Collectors.groupingBy(
                Employee::getDepartment,
                Collectors.collectingAndThen(
                    Collectors.maxBy(Comparator.comparingDouble(Employee::getSalary)), 
                    Optional::get 
                )
            ));

        System.out.println("2. Highest Paid Employee in Each Department:");
        topPaidPerDept.forEach((dept, emp) -> 
            System.out.println("   - " + dept + ": " + emp.getName() + " ($" + emp.getSalary() + ")")
        );
        System.out.println();

        String recentEmployees = employees.stream()
            .filter(e -> e.getYearJoined() > 2019)
            .map(Employee::getName)
            .sorted()
            .collect(Collectors.joining(", "));

        System.out.println("3. Employees Joined After 2019 (Sorted Alphabetically):");
        System.out.println("   -> " + recentEmployees);
    }
}