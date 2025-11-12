import pandas as pd
from pathlib import Path 

DATA_DIR = Path(__file__).resolve().parents[1]

def add_time_features(df):
    """
    Add calender based feature derived from date
    """
    df["dayofweek"]= df["date"].dt.dayofweek 
    df["month"]= df["date"].dt.month 
    df["year"]= df["date"].dt.year 
    
