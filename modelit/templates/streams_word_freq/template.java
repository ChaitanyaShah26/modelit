import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class WordFrequencyDemo {
    public static void main(String[] args) {
        Path filePath = Path.of("sample_paragraph.txt");
        generateTestFile(filePath);

        System.out.println("--- WORD FREQUENCY ANALYZER ---\n");

        try (Stream<String> lines = Files.lines(filePath)) {
            
            Map<String, Long> wordCounts = lines
                .flatMap(line -> Arrays.stream(line.split("\\W+")))
                .filter(word -> !word.isEmpty())
                .map(String::toLowerCase) 
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));

            System.out.println("1. Top 10 Most Frequent Words:");
            wordCounts.entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
                .limit(10)
                .forEach(e -> System.out.printf("   - '%s': %d times\n", e.getKey(), e.getValue()));
            System.out.println();

            List<String> exactlyOnce = wordCounts.entrySet().stream()
                .filter(e -> e.getValue() == 1)
                .map(Map.Entry::getKey)
                .sorted()
                .collect(Collectors.toList());
            
            System.out.println("2. Words appearing exactly once (" + exactlyOnce.size() + " words):");
            System.out.println("   " + String.join(", ", exactlyOnce) + "\n");

            long longWordsCount = wordCounts.keySet().stream()
                .filter(word -> word.length() > 6)
                .count();
            
            System.out.println("3. Number of unique words longer than 6 characters: " + longWordsCount);

        } catch (IOException e) {
            System.err.println("Error reading the file: " + e.getMessage());
        }
    }

    private static void generateTestFile(Path path) {
        String content = "Sample Text";
        try { 
            Files.writeString(path, content); 
        } catch (IOException e) {
            System.err.println("Could not create test file.");
        }
    }
}