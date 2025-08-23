import sys
import os

# Add the parent directory to the path to import PreProcessing
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(parent_dir)

from PreProcessing.PreProcessing import PreProcessing

class PreProcessingSingleton:
    _instance = None
    _preprocessing = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PreProcessingSingleton, cls).__new__(cls)
            cls._preprocessing = PreProcessing()
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of PreProcessing"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._preprocessing

# Global function to get preprocessing instance
def get_preprocessing():
    """Get the global PreProcessing instance"""
    return PreProcessingSingleton.get_instance()