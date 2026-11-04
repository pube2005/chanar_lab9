package mn.edu.must.sqat;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ScholarshipCalculatorTest {
    private final ScholarshipCalculator calculator = new ScholarshipCalculator();

    @Test void letterGrade_highScore_returnsA() {
        assertEquals("A", calculator.letterGrade(95));
    }
    @Test void letterGrade_middleScore_returnsC() {
        assertEquals("C", calculator.letterGrade(75));
    }
    @Test void gpa_twoGrades_returnsMean() {
        assertEquals(3.5, calculator.gpa(new double[]{95, 85}), 1e-12);
    }
    @Test void scholarship_highGpaEnoughCredits_returns100() {
        assertEquals(100, calculator.scholarship(3.9, 16, false));
    }
    @Test void scholarship_middleGpaEnoughCredits_returns70() {
        assertEquals(70, calculator.scholarship(3.5, 12, false));
    }
}
