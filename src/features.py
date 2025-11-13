import pandas as pd
from pathlib import Path 

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

def add_time_features(df):
    """
    Add calender based feature derived from date
    """
    df["dayofweek"]= df["date"].dt.dayofweek 
    df["month"]= df["date"].dt.month 
    df["year"]= df["date"].dt.year 
    df["is_weakend"]= df["dayofweek"].isin([5,6]).astype(int) 
    return df  

def create_features():
    """ create lag and rolling stastistics features """
    df= pd.read_csv(DATA_DIR/"train_full.csv",parse_dates=["date"])
    df= add_time_features(df)

    # sort to proper calculation of lag 

    df= df.sort_values(["store","dept","date"])
    grp= df.groupby(["store","dept"])

    # lag features: previous 1 and 7 weak's sales 

    df["lag_1"] = grp["weekly_sales"].shift(1)
    df["lag_7"]= grp["weekly_sales"].shift(7)

    # rolling average past 7 weeks 
    df["roll_mean_7"] = (
        grp["weekly_sales"]
        .shift(1)
        .rolling(7, min_periods=1)
        .mean()
        .reset_index(drop=True)
    )


    df.fillna(0,inplace=True)

    # save to processed folder 
    df.to_csv(DATA_DIR/"train_features.csv",index=False)
    print("✅ Feature file created at:", DATA_DIR)

if __name__ == "__main__":
    create_features()

