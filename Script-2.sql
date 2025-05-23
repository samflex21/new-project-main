SELECT COUNT(*) AS TotalPatients FROM Patient;

SELECT AVG(BMI) AS AverageBMI FROM VitalSigns;

SELECT 
    Patient.PatientID,
    LabResults.Cholesterol_Level,
    RiskAssessment.StressLevel_Category
FROM 
    Patient
JOIN LabResults ON Patient.PatientID = LabResults.PatientID
JOIN RiskAssessment ON Patient.PatientID = RiskAssessment.PatientID;

SELECT 
    COUNT(*) AS ObeseHighRiskCount
FROM 
    Lifestyle
JOIN RiskAssessment ON Lifestyle.PatientID = RiskAssessment.PatientID
WHERE 
    Obesity = 1 AND HeartAttackRiskBinary = 1;

SELECT 
    Patient.PatientID,
    VitalSigns.BMI,
    RiskAssessment.HeartAttackRiskBinary,
    PredictionLog.ModelUsed,
    PredictionLog.PredictedRisk
FROM 
    Patient
JOIN VitalSigns ON Patient.PatientID = VitalSigns.PatientID
JOIN RiskAssessment ON Patient.PatientID = RiskAssessment.PatientID
JOIN PredictionLog ON Patient.PatientID = PredictionLog.PatientID
WHERE 
    VitalSigns.BMI_Level = 'High'
    AND RiskAssessment.HeartAttackRiskBinary = 1
    AND PredictionLog.PredictedRisk > 0.7
ORDER BY PredictionLog.PredictedRisk DESC;
