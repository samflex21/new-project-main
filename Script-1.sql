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


