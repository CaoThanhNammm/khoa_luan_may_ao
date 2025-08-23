"""
Global instances and configurations for the application
"""
from app.utils.preprocessing_singleton import get_preprocessing

# Initialize global instances when the module is imported
preprocessing_instance = get_preprocessing()

def get_global_preprocessing():
    """Get the global preprocessing instance"""
    return preprocessing_instance