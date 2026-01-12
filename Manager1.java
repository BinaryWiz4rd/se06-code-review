/**
 * The Manager1 class implements the following requirements:
 * 1/ The system should validate the patient's age using defined limits and stop processing if the age is outside of the valid range.
 * 2/ The system should classify the patient's blood pressure (BP) reading as high risk (systolic BP > 150 and diastolic BP > 95), medium risk (systolic BP > 130), or normal.
 * 3/ The system should output the result for further processing.
 */

import java.io.FileWriter;
import java.io.*;
import java.util.*;

public class Manager1 {

    private final PatientRepository repository = new PatientRepository();
    private final HealthAssessmentService healthService = new HealthAssessmentService();

    public void process(Patient1 p) {

        if (!healthService.isValidAge(p.getAge())) {
            System.out.println("Invalid age!");
            repository.log("Invalid patient: " + p.getName());
            return;
        }

        if (healthService.isMinor(p.getAge())) {
            System.out.println("Patient is a minor.");
        } else {
            System.out.println("Patient is an adult.");
        }

        repository.log("Processed patient " + p.getName());
    }

    public int process2(
            Patient1 p,
            int bpSys,
            int bpDia,
            boolean printResult
    ) {
        if (!healthService.isValidAge(p.getAge())) {
            repository.log("Invalid patient age: " + p.getAge());
            return -1;
        }

        int result = healthService.assessBloodPressure(bpSys, bpDia);

        if (printResult) {
            System.out.println("Patient " + p.getName() + ": score=" + result);
        }

        return result;
    }
}

class HealthAssessmentService {
    private static final int MIN_AGE = 0;
    private static final int MAX_AGE = 130;
    private static final int ADULT_AGE = 18;

    public boolean isValidAge(int age) {
        return age >= MIN_AGE && age <= MAX_AGE;
    }

    public boolean isMinor(int age) {
        return age < ADULT_AGE;
    }

    public int assessBloodPressure(int bpSys, int bpDia) {
        if (bpSys > 150 || bpDia > 95) {
            return 2;
        } else if (bpSys > 130) {
            return 1;
        } else {
            return 0;
        }
    }
}

class PatientRepository {
    private List<String> logs = new ArrayList<>();

    private static final String DB_URL = "jdbc:mysql://localhost:3306/hospital";
    private static final String REPORT_FILE = "report.txt";

    public void log(String message) {
        logs.add(message);
    }

    public List<String> getLogs() {
        return logs;
    }
}

class Patient1 {
    private String name;
    private int age;
    private String existing_condition;

    public Patient1(String name, int age, String condition) {
        this.name = name;
        this.age = age;
        this.existing_condition = condition;
    }
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getExistingCondition() {
        return existing_condition;
    }

    public void setExistingCondition(String existing_condition) {
        this.existing_condition = existing_condition;
    }
}
