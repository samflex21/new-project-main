import os

class Config:
    """Configuration settings for the application"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-heart-risk-dashboard'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///heart_risk_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    DATA_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'Heart_Attack_Predicted_Levels_Only.csv')
    
    # Dashboard settings
    ITEMS_PER_PAGE = 20
    CACHE_TIMEOUT = 300  # 5 minutes cache timeout
    
    # Debug settings
    DEBUG_TB_INTERCEPT_REDIRECTS = False
