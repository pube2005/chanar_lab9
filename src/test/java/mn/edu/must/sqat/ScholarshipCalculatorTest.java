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

    @Test void letterGrade_negativeScore_throws() {
        assertThrows(IllegalArgumentException.class, () -> calculator.letterGrade(-1));
    }
    @Test void letterGrade_aboveMaximum_throws() {
        assertThrows(IllegalArgumentException.class, () -> calculator.letterGrade(101));
    }
    @Test void letterGrade_sixtyFive_returnsD() {
        assertEquals("D", calculator.letterGrade(65));
    }
    @Test void letterGrade_lowScore_returnsF() {
        assertEquals("F", calculator.letterGrade(50));
    }
    @Test void gpa_nullScores_throws() {
        assertThrows(IllegalArgumentException.class, () -> calculator.gpa(null));
    }
    @Test void gpa_emptyScores_throws() {
        assertThrows(IllegalArgumentException.class, () -> calculator.gpa(new double[]{}));
    }
    @Test void gpa_allGradeCategories_returnsMean() {
        assertEquals(2.0, calculator.gpa(new double[]{95, 85, 75, 65, 50}), 1e-12);
    }
    @Test void scholarship_negativeGpa_throws() {
        assertThrows(IllegalArgumentException.class, () -> calculator.scholarship(-0.1, 15, false));
    }
    @Test void scholarship_gpaAboveFour_throws() {
        assertThrows(IllegalArgumentException.class, () -> calculator.scholarship(4.1, 15, false));
    }
    @Test void scholarship_negativeCredits_throws() {
        assertThrows(IllegalArgumentException.class, () -> calculator.scholarship(3.5, -1, false));
    }
    @Test void scholarship_violation_returns0() {
        assertEquals(0, calculator.scholarship(4.0, 18, true));
    }
    @Test void scholarship_highGpaTooFewFor100_returns70() {
        assertEquals(70, calculator.scholarship(3.8, 14, false));
    }
    @Test void scholarship_middleGpaTooFewFor70_returns50() {
        assertEquals(50, calculator.scholarship(3.4, 11, false));
    }
    @Test void scholarship_threeGpa_returns50() {
        assertEquals(50, calculator.scholarship(3.0, 0, false));
    }
    @Test void scholarship_lowGpa_returns0() {
        assertEquals(0, calculator.scholarship(0.0, 0, false));
    }
}
