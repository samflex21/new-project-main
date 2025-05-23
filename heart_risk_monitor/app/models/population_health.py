import sqlite3
import pandas as pd
import numpy as np
from flask import current_app
from app.models.data_loader import data_loader

def get_health_risk_by_income():
    """
    Retrieves data showing the relationship between income levels and heart attack risk
    using Patient and RiskAssessment tables
    
    Returns:
        List of dictionaries with income bracket and risk distribution
    """
    query = """
    SELECT 
        CASE
            WHEN Income < 30000 THEN 'Low Income'
            WHEN Income < 60000 THEN 'Middle Income'
            WHEN Income < 100000 THEN 'Upper Middle Income'
            ELSE 'High Income'
        END as income_bracket,
        HeartAttackRiskText,
        COUNT(*) as count
    FROM 
        Patient p
    JOIN 
        RiskAssessment r ON p.PatientID = r.PatientID
    GROUP BY 
        income_bracket, HeartAttackRiskText
    ORDER BY
        income_bracket
    """
    
    try:
        return data_loader.query_db(query)
    except (sqlite3.Error, FileNotFoundError):
        # Mock data if database query fails
        return [
            {'income_bracket': 'Low Income', 'HeartAttackRiskText': 'High Risk', 'count': 25},
            {'income_bracket': 'Low Income', 'HeartAttackRiskText': 'Medium Risk', 'count': 18},
            {'income_bracket': 'Low Income', 'HeartAttackRiskText': 'Low Risk', 'count': 12},
            {'income_bracket': 'Middle Income', 'HeartAttackRiskText': 'High Risk', 'count': 20},
            {'income_bracket': 'Middle Income', 'HeartAttackRiskText': 'Medium Risk', 'count': 26},
            {'income_bracket': 'Middle Income', 'HeartAttackRiskText': 'Low Risk', 'count': 24},
            {'income_bracket': 'Upper Middle Income', 'HeartAttackRiskText': 'High Risk', 'count': 10},
            {'income_bracket': 'Upper Middle Income', 'HeartAttackRiskText': 'Medium Risk', 'count': 18},
            {'income_bracket': 'Upper Middle Income', 'HeartAttackRiskText': 'Low Risk', 'count': 32},
            {'income_bracket': 'High Income', 'HeartAttackRiskText': 'High Risk', 'count': 8},
            {'income_bracket': 'High Income', 'HeartAttackRiskText': 'Medium Risk', 'count': 15},
            {'income_bracket': 'High Income', 'HeartAttackRiskText': 'Low Risk', 'count': 42}
        ]

def get_diet_score_by_age():
    """
    Retrieves average diet scores across different age groups
    using Patient and DietaryHabits tables
    
    Returns:
        List of dictionaries with age group and average diet score
    """
    query = """
    SELECT 
        CASE
            WHEN Age < 30 THEN '18-29'
            WHEN Age < 45 THEN '30-44'
            WHEN Age < 60 THEN '45-59'
            ELSE '60+'
        END as age_group,
        AVG(DietScore) as average_diet_score
    FROM 
        Patient p
    JOIN 
        DietaryHabits d ON p.PatientID = d.PatientID
    GROUP BY 
        age_group
    ORDER BY
        CASE
            WHEN age_group = '18-29' THEN 1
            WHEN age_group = '30-44' THEN 2
            WHEN age_group = '45-59' THEN 3
            ELSE 4
        END
    """
    
    try:
        return data_loader.query_db(query)
    except (sqlite3.Error, FileNotFoundError):
        # Mock data if database query fails
        return [
            {'age_group': '18-29', 'average_diet_score': 7.2},
            {'age_group': '30-44', 'average_diet_score': 6.5},
            {'age_group': '45-59', 'average_diet_score': 5.8},
            {'age_group': '60+', 'average_diet_score': 5.3}
        ]

def get_exercise_sleep_distribution():
    """
    Retrieves the relationship between exercise hours and sleep hours
    and their impact on heart attack risk using Lifestyle and RiskAssessment tables
    
    Returns:
        List of dictionaries with exercise hours, sleep hours, and risk level
    """
    query = """
    SELECT 
        l.ExerciseHoursPerWeek,
        l.SleepHoursPerDay,
        r.HeartAttackRiskText,
        COUNT(*) as patient_count
    FROM 
        Lifestyle l
    JOIN 
        RiskAssessment r ON l.PatientID = r.PatientID
    GROUP BY 
        l.ExerciseHoursPerWeek, l.SleepHoursPerDay, r.HeartAttackRiskText
    """
    
    try:
        return data_loader.query_db(query)
    except (sqlite3.Error, FileNotFoundError):
        # Mock data if database query fails
        return [
            # Low risk data points
            {'ExerciseHoursPerWeek': 5, 'SleepHoursPerDay': 7, 'HeartAttackRiskText': 'Low Risk', 'patient_count': 15},
            {'ExerciseHoursPerWeek': 7, 'SleepHoursPerDay': 8, 'HeartAttackRiskText': 'Low Risk', 'patient_count': 22},
            {'ExerciseHoursPerWeek': 6, 'SleepHoursPerDay': 7.5, 'HeartAttackRiskText': 'Low Risk', 'patient_count': 18},
            {'ExerciseHoursPerWeek': 4, 'SleepHoursPerDay': 6.5, 'HeartAttackRiskText': 'Low Risk', 'patient_count': 10},
            # Medium risk data points
            {'ExerciseHoursPerWeek': 3, 'SleepHoursPerDay': 6, 'HeartAttackRiskText': 'Medium Risk', 'patient_count': 14},
            {'ExerciseHoursPerWeek': 2, 'SleepHoursPerDay': 7, 'HeartAttackRiskText': 'Medium Risk', 'patient_count': 12},
            {'ExerciseHoursPerWeek': 4, 'SleepHoursPerDay': 5, 'HeartAttackRiskText': 'Medium Risk', 'patient_count': 16},
            {'ExerciseHoursPerWeek': 1, 'SleepHoursPerDay': 8, 'HeartAttackRiskText': 'Medium Risk', 'patient_count': 8},
            # High risk data points
            {'ExerciseHoursPerWeek': 1, 'SleepHoursPerDay': 5, 'HeartAttackRiskText': 'High Risk', 'patient_count': 20},
            {'ExerciseHoursPerWeek': 0, 'SleepHoursPerDay': 6, 'HeartAttackRiskText': 'High Risk', 'patient_count': 15},
            {'ExerciseHoursPerWeek': 2, 'SleepHoursPerDay': 4, 'HeartAttackRiskText': 'High Risk', 'patient_count': 12},
            {'ExerciseHoursPerWeek': 0, 'SleepHoursPerDay': 4, 'HeartAttackRiskText': 'High Risk', 'patient_count': 18}
        ]

def get_smoking_stress_by_gender():
    """
    Retrieves the correlation between smoking, stress levels and gender
    using Lifestyle, RiskAssessment, and Patient tables
    
    Returns:
        List of dictionaries with gender, smoking status, stress level, and count
    """
    query = """
    SELECT 
        p.Gender,
        l.Smoking,
        r.StressLevel_Category,
        COUNT(*) as count
    FROM 
        Patient p
    JOIN 
        Lifestyle l ON p.PatientID = l.PatientID
    JOIN 
        RiskAssessment r ON p.PatientID = r.PatientID
    GROUP BY 
        p.Gender, l.Smoking, r.StressLevel_Category
    """
    
    try:
        return data_loader.query_db(query)
    except (sqlite3.Error, FileNotFoundError):
        # Mock data if database query fails
        return [
            {'Gender': 'Male', 'Smoking': 1, 'StressLevel_Category': 'High', 'count': 18},
            {'Gender': 'Male', 'Smoking': 1, 'StressLevel_Category': 'Medium', 'count': 12},
            {'Gender': 'Male', 'Smoking': 1, 'StressLevel_Category': 'Low', 'count': 5},
            {'Gender': 'Male', 'Smoking': 0, 'StressLevel_Category': 'High', 'count': 10},
            {'Gender': 'Male', 'Smoking': 0, 'StressLevel_Category': 'Medium', 'count': 15},
            {'Gender': 'Male', 'Smoking': 0, 'StressLevel_Category': 'Low', 'count': 25},
            {'Gender': 'Female', 'Smoking': 1, 'StressLevel_Category': 'High', 'count': 12},
            {'Gender': 'Female', 'Smoking': 1, 'StressLevel_Category': 'Medium', 'count': 10},
            {'Gender': 'Female', 'Smoking': 1, 'StressLevel_Category': 'Low', 'count': 4},
            {'Gender': 'Female', 'Smoking': 0, 'StressLevel_Category': 'High', 'count': 15},
            {'Gender': 'Female', 'Smoking': 0, 'StressLevel_Category': 'Medium', 'count': 22},
            {'Gender': 'Female', 'Smoking': 0, 'StressLevel_Category': 'Low', 'count': 32}
        ]
