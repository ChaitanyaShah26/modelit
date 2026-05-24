abstract class DataExportPipeline {
    public final void runPipeline() {
        extractData();
        transformData();
        exportData();
        System.out.println("Pipeline execution completed.\n");
    }

    protected void extractData() {
        System.out.println("Extracting data from SQL Database...");
    }
    
    protected void transformData() {
        System.out.println("Transforming and cleansing raw data...");
    }

    protected abstract void exportData();
}

class JSONExporter extends DataExportPipeline {
    protected void exportData() {
        System.out.println("Exporting transformed data into a .JSON file");
    }
}

class CSVExporter extends DataExportPipeline {
    protected void exportData() {
        System.out.println("Exporting transformed data into a .CSV file");
    }
}

public class TemplateDemo {
    public static void main(String[] args) {
        DataExportPipeline jsonJob = new JSONExporter();
        jsonJob.runPipeline();

        DataExportPipeline csvJob = new CSVExporter();
        csvJob.runPipeline();
    }
}