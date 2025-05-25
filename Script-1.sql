-- Schema Definition
CREATE TABLE Patient (
    PatientID INTEGER PRIMARY KEY,
    Age INTEGER,
    Gender TEXT,
    Income DECIMAL
);

CREATE TABLE VitalSigns (
    VitalSignID INTEGER PRIMARY KEY,
    PatientID INTEGER,
    SystolicBP INTEGER,
    SystolicBP_Level TEXT,
    HeartRate INTEGER,
    DiastolicBP INTEGER,
    DiastolicBP_Level TEXT,
    BMI DECIMAL,
    BMI_Level TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE LabResults (
    LabID INTEGER PRIMARY KEY,
    PatientID INTEGER,
    Cholesterol DECIMAL,
    Cholesterol_Level TEXT,
    BloodSugar DECIMAL,
    BloodSugar_Level TEXT,
    Triglycerides DECIMAL,
    CK_MB DECIMAL,
    CK_MB_Level TEXT,
    Troponin DECIMAL,
    Troponin_Level TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE Lifestyle (
    LifestyleID INTEGER PRIMARY KEY,
    PatientID INTEGER,
    Smoking BOOLEAN,
    AlcoholConsumption BOOLEAN,
    ExerciseHoursPerWeek INTEGER,
    Diet TEXT,
    SleepHoursPerDay INTEGER,
    SedentaryHoursPerDay INTEGER,
    Obesity BOOLEAN,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE MedicalHistory (
    HistoryID INTEGER PRIMARY KEY,
    PatientID INTEGER UNIQUE,
    Diabetes BOOLEAN,
    FamilyHistory BOOLEAN,
    PreviousHeartProblems BOOLEAN,
    MedicationUse BOOLEAN,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE RiskAssessment (
    AssessmentID INTEGER PRIMARY KEY,
    PatientID INTEGER,
    StressLevel TEXT,
    StressLevel_Category TEXT,
    HeartAttackRiskBinary BOOLEAN,
    HeartAttackRiskText TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE DietaryHabits (
    ActivityID INTEGER PRIMARY KEY,
    PatientID INTEGER,
    DietType TEXT,
    DietScore INTEGER,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE PredictionLog (
    PredictionID INTEGER PRIMARY KEY,
    PatientID INTEGER,
    PredictionDate DATETIME,
    PredictedRisk DECIMAL,
    ModelUsed TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

-- Sample Data Population
-- Insert Patient Data with different income levels and age groups
INSERT INTO Patient (PatientID, Age, Gender, Income) VALUES
-- Low Income Group
(1, 25, 'Male', 25000),
(2, 32, 'Female', 28000),
(3, 45, 'Male', 29000),
(4, 56, 'Female', 27000),
(5, 68, 'Male', 26000),
(6, 22, 'Female', 24000),
(7, 35, 'Male', 29500),
(8, 47, 'Female', 28200),
(9, 62, 'Male', 27800),
(10, 29, 'Female', 25400),

-- Middle Income Group
(11, 27, 'Male', 45000),
(12, 34, 'Female', 48000),
(13, 46, 'Male', 52000),
(14, 58, 'Female', 47000),
(15, 70, 'Male', 46000),
(16, 24, 'Female', 44000),
(17, 36, 'Male', 49500),
(18, 48, 'Female', 51200),
(19, 63, 'Male', 47800),
(20, 31, 'Female', 45400),

-- Upper Middle Income Group
(21, 28, 'Male', 75000),
(22, 36, 'Female', 78000),
(23, 48, 'Male', 82000),
(24, 59, 'Female', 77000),
(25, 71, 'Male', 76000),
(26, 26, 'Female', 74000),
(27, 38, 'Male', 79500),
(28, 50, 'Female', 81200),
(29, 64, 'Male', 77800),
(30, 33, 'Female', 75400),

-- High Income Group
(31, 30, 'Male', 95000),
(32, 37, 'Female', 98000),
(33, 49, 'Male', 110000),
(34, 60, 'Female', 105000),
(35, 72, 'Male', 120000),
(36, 27, 'Female', 94000),
(37, 39, 'Male', 99500),
(38, 51, 'Female', 101200),
(39, 65, 'Male', 107800),
(40, 34, 'Female', 95400);

-- Insert Risk Assessment Data
INSERT INTO RiskAssessment (AssessmentID, PatientID, StressLevel, StressLevel_Category, HeartAttackRiskBinary, HeartAttackRiskText) VALUES
-- Low Income Group - mix of risk levels but higher proportion of high risk
(1, 1, 'High', 'High', 1, 'High Risk'),
(2, 2, 'Medium', 'Medium', 1, 'High Risk'),
(3, 3, 'High', 'High', 1, 'High Risk'),
(4, 4, 'Medium', 'Medium', 0, 'Medium Risk'),
(5, 5, 'Low', 'Low', 0, 'Low Risk'),
(6, 6, 'High', 'High', 1, 'High Risk'),
(7, 7, 'Medium', 'Medium', 0, 'Medium Risk'),
(8, 8, 'Medium', 'Medium', 1, 'High Risk'),
(9, 9, 'Low', 'Low', 0, 'Low Risk'),
(10, 10, 'High', 'High', 1, 'High Risk'),

-- Middle Income Group - mix of risk levels
(11, 11, 'Medium', 'Medium', 1, 'High Risk'),
(12, 12, 'Low', 'Low', 0, 'Medium Risk'),
(13, 13, 'Medium', 'Medium', 0, 'Medium Risk'),
(14, 14, 'High', 'High', 1, 'High Risk'),
(15, 15, 'Low', 'Low', 0, 'Low Risk'),
(16, 16, 'Medium', 'Medium', 0, 'Medium Risk'),
(17, 17, 'Low', 'Low', 0, 'Medium Risk'),
(18, 18, 'Medium', 'Medium', 0, 'Medium Risk'),
(19, 19, 'Low', 'Low', 0, 'Low Risk'),
(20, 20, 'High', 'High', 1, 'High Risk'),

-- Upper Middle Income Group - better risk profile
(21, 21, 'Low', 'Low', 0, 'Medium Risk'),
(22, 22, 'Medium', 'Medium', 0, 'Medium Risk'),
(23, 23, 'Low', 'Low', 0, 'Low Risk'),
(24, 24, 'Medium', 'Medium', 0, 'Medium Risk'),
(25, 25, 'Low', 'Low', 0, 'Low Risk'),
(26, 26, 'High', 'High', 1, 'High Risk'),
(27, 27, 'Low', 'Low', 0, 'Low Risk'),
(28, 28, 'Medium', 'Medium', 0, 'Medium Risk'),
(29, 29, 'Low', 'Low', 0, 'Low Risk'),
(30, 30, 'Medium', 'Medium', 0, 'Medium Risk'),

-- High Income Group - lowest risk profile
(31, 31, 'Low', 'Low', 0, 'Low Risk'),
(32, 32, 'Medium', 'Medium', 0, 'Medium Risk'),
(33, 33, 'Low', 'Low', 0, 'Low Risk'),
(34, 34, 'Medium', 'Medium', 0, 'Medium Risk'),
(35, 35, 'Low', 'Low', 0, 'Low Risk'),
(36, 36, 'Low', 'Low', 0, 'Low Risk'),
(37, 37, 'Medium', 'Medium', 0, 'Medium Risk'),
(38, 38, 'Low', 'Low', 0, 'Low Risk'),
(39, 39, 'Low', 'Low', 0, 'Low Risk'),
(40, 40, 'High', 'High', 1, 'High Risk');

-- Insert Dietary Habits Data - diet score tends to increase with age
INSERT INTO DietaryHabits (ActivityID, PatientID, DietType, DietScore) VALUES
-- Age Group 18-29
(1, 1, 'Mixed', 6),
(2, 6, 'Vegetarian', 7),
(3, 10, 'Mixed', 5),
(4, 11, 'Mixed', 6),
(5, 16, 'Pescatarian', 7),
(6, 21, 'Mixed', 6),
(7, 26, 'Vegetarian', 7),
(8, 31, 'Mixed', 6),
(9, 36, 'Mixed', 6),

-- Age Group 30-44
(10, 2, 'Mixed', 6),
(11, 7, 'Vegetarian', 7),
(12, 12, 'Mixed', 7),
(13, 17, 'Mixed', 7),
(14, 22, 'Vegetarian', 8),
(15, 27, 'Mixed', 6),
(16, 32, 'Pescatarian', 8),
(17, 37, 'Mixed', 7),
(18, 40, 'Mixed', 7),

-- Age Group 45-59
(19, 3, 'Mixed', 7),
(20, 8, 'Vegetarian', 8),
(21, 13, 'Mixed', 7),
(22, 18, 'Pescatarian', 8),
(23, 23, 'Mixed', 7),
(24, 28, 'Vegetarian', 8),
(25, 33, 'Mixed', 7),
(26, 38, 'Mixed', 7),

-- Age Group 60+
(27, 4, 'Mediterranean', 8),
(28, 5, 'Mixed', 8),
(29, 9, 'Mediterranean', 8),
(30, 14, 'Vegetarian', 8),
(31, 15, 'Mediterranean', 9),
(32, 19, 'Mixed', 7),
(33, 20, 'Mixed', 7),
(34, 24, 'Mediterranean', 8),
(35, 25, 'Mixed', 7),
(36, 29, 'Mediterranean', 9),
(37, 30, 'Mixed', 7),
(38, 34, 'Mediterranean', 8),
(39, 35, 'Vegetarian', 9),
(40, 39, 'Mixed', 8);

-- Insert Lifestyle Data for exercise vs sleep distribution
INSERT INTO Lifestyle (LifestyleID, PatientID, Smoking, AlcoholConsumption, ExerciseHoursPerWeek, Diet, SleepHoursPerDay, SedentaryHoursPerDay, Obesity) VALUES
-- High Risk patients (typically low exercise, low/high sleep)
(1, 1, 1, 1, 1, 'Poor', 5, 12, 1),
(2, 3, 1, 1, 0, 'Poor', 4, 14, 1),
(3, 6, 0, 1, 2, 'Poor', 5, 10, 1),
(4, 8, 1, 0, 1, 'Average', 6, 11, 1),
(5, 10, 1, 1, 2, 'Poor', 5, 12, 1),
(6, 11, 1, 1, 2, 'Poor', 5, 10, 0),
(7, 14, 0, 1, 1, 'Poor', 4, 11, 1),
(8, 26, 1, 0, 2, 'Average', 5, 12, 1),
(9, 40, 1, 1, 0, 'Poor', 4, 14, 1),

-- Medium Risk patients (moderate exercise, varied sleep)
(10, 2, 0, 1, 3, 'Average', 6, 8, 0),
(11, 4, 0, 1, 4, 'Good', 7, 7, 0),
(12, 7, 1, 0, 3, 'Average', 6, 9, 0),
(13, 12, 0, 1, 3, 'Average', 7, 8, 0),
(14, 13, 0, 0, 4, 'Good', 8, 8, 0),
(15, 16, 0, 1, 3, 'Average', 6, 8, 0),
(16, 17, 1, 0, 4, 'Average', 6, 7, 0),
(17, 18, 0, 1, 5, 'Good', 7, 6, 0),
(18, 20, 0, 1, 3, 'Average', 6, 8, 0),
(19, 21, 0, 0, 4, 'Good', 7, 7, 0),
(20, 22, 0, 1, 3, 'Average', 6, 8, 0),
(21, 24, 0, 0, 5, 'Good', 8, 6, 0),
(22, 28, 0, 1, 4, 'Good', 7, 7, 0),
(23, 30, 0, 1, 3, 'Average', 6, 8, 0),
(24, 32, 0, 0, 4, 'Good', 7, 7, 0),
(25, 37, 0, 1, 3, 'Average', 6, 8, 0),

-- Low Risk patients (higher exercise, good sleep)
(26, 5, 0, 0, 6, 'Good', 7, 5, 0),
(27, 9, 0, 0, 7, 'Excellent', 8, 4, 0),
(28, 15, 0, 0, 5, 'Good', 7, 6, 0),
(29, 19, 0, 0, 6, 'Good', 8, 5, 0),
(30, 23, 0, 0, 7, 'Excellent', 8, 4, 0),
(31, 25, 0, 0, 6, 'Good', 7, 5, 0),
(32, 27, 0, 0, 7, 'Excellent', 8, 4, 0),
(33, 29, 0, 0, 5, 'Good', 7, 6, 0),
(34, 31, 0, 0, 6, 'Excellent', 8, 5, 0),
(35, 33, 0, 0, 7, 'Excellent', 8, 4, 0),
(36, 34, 0, 0, 5, 'Good', 7, 6, 0),
(37, 35, 0, 0, 8, 'Excellent', 8, 3, 0),
(38, 36, 0, 0, 6, 'Good', 7, 5, 0),
(39, 38, 0, 0, 5, 'Good', 7, 6, 0),
(40, 39, 0, 0, 6, 'Excellent', 8, 5, 0);

-- SQL Queries for Dashboard Charts

-- 1. Health Risk by Income Level - Stacked Bar Chart
-- Query to get health risk distribution across income brackets
SELECT 
    CASE 
        WHEN p.Income < 30000 THEN 'Low Income'
        WHEN p.Income >= 30000 AND p.Income < 60000 THEN 'Middle Income'
        WHEN p.Income >= 60000 AND p.Income < 90000 THEN 'Upper Middle Income'
        ELSE 'High Income'
    END AS income_bracket,
    ra.HeartAttackRiskText,
    COUNT(*) AS count
FROM 
    Patient p
    JOIN RiskAssessment ra ON p.PatientID = ra.PatientID
GROUP BY 
    income_bracket, ra.HeartAttackRiskText
ORDER BY 
    CASE income_bracket
        WHEN 'Low Income' THEN 1
        WHEN 'Middle Income' THEN 2
        WHEN 'Upper Middle Income' THEN 3
        WHEN 'High Income' THEN 4
    END,
    CASE ra.HeartAttackRiskText
        WHEN 'High Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'Low Risk' THEN 3
    END;

-- 2. Average Diet Score by Age Group - Line Chart
-- Query to get average diet score for different age groups
SELECT 
    CASE 
        WHEN p.Age BETWEEN 18 AND 29 THEN '18-29'
        WHEN p.Age BETWEEN 30 AND 44 THEN '30-44'
        WHEN p.Age BETWEEN 45 AND 59 THEN '45-59'
        ELSE '60+'
    END AS age_group,
    AVG(dh.DietScore) AS average_score
FROM 
    Patient p
    JOIN DietaryHabits dh ON p.PatientID = dh.PatientID
GROUP BY 
    age_group
ORDER BY 
    CASE age_group
        WHEN '18-29' THEN 1
        WHEN '30-44' THEN 2
        WHEN '45-59' THEN 3
        WHEN '60+' THEN 4
    END;

-- 3. Exercise vs Sleep Distribution - Scatter Plot
-- Query to get exercise hours vs sleep hours with risk level
SELECT 
    l.ExerciseHoursPerWeek AS exercise_hours, 
    l.SleepHoursPerDay AS sleep_hours,
    ra.HeartAttackRiskText AS risk_level,
    COUNT(*) AS patient_count
FROM 
    Lifestyle l
    JOIN RiskAssessment ra ON l.PatientID = ra.PatientID
GROUP BY 
    l.ExerciseHoursPerWeek, l.SleepHoursPerDay, ra.HeartAttackRiskText
ORDER BY 
    l.ExerciseHoursPerWeek, l.SleepHoursPerDay;

-- 4. Smoking & Stress by Gender - Grouped Column Chart
-- Query to get stress levels distribution by gender and smoking status
SELECT 
    p.Gender AS gender,
    CASE WHEN l.Smoking = 1 THEN 'Smoker' ELSE 'Non-Smoker' END AS smoking_status,
    ra.StressLevel AS stress_level,
    COUNT(*) AS count
FROM 
    Patient p
    JOIN Lifestyle l ON p.PatientID = l.PatientID
    JOIN RiskAssessment ra ON p.PatientID = ra.PatientID
GROUP BY 
    p.Gender, smoking_status, ra.StressLevel
ORDER BY 
    p.Gender, smoking_status,
    CASE ra.StressLevel
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
    END;

-- Additional Queries for Dashboard Statistics

-- Total Patient Count
SELECT COUNT(*) AS total_patients FROM Patient;

-- Average Age
SELECT AVG(Age) AS average_age FROM Patient;

-- High Risk Percentage
SELECT 
    (COUNT(CASE WHEN HeartAttackRiskText = 'High Risk' THEN 1 END) * 100.0 / COUNT(*)) AS high_risk_percentage
FROM 
    RiskAssessment;

-- Risk Assessment Completion Rate
SELECT 
    (SELECT COUNT(*) FROM RiskAssessment) AS completed_assessments,
    (SELECT COUNT(*) FROM Patient) AS total_patients;
