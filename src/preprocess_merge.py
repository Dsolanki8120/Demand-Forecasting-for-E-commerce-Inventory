import pandas as pd 
from pathlib import Path

# merge csv file 


BASE_DIR= Path(__file__).resolve().parent.parent
DATA_DIR= BASE_DIR/ "data"
OUT_DIR= DATA_DIR/"processed"
OUT_DIR.mkdir(exist_ok=True)   # create folder if missing

def load_data():
    """ load all data file into one pandas dataframe """
    train= pd.read_csv(DATA_DIR/"train.csv",parse_dates=["Date"])
    features= pd.read_csv(DATA_DIR/"features.csv",parse_dates=["Date"])
    stores= pd.read_csv(DATA_DIR/"stores.csv")
    test= pd.read_csv(DATA_DIR/"test.csv",parse_dates=["Date"])
    return train,features,stores,test 
def merge_and_clean():

    """
         Merge CSV file and clean missing data 
    """
    # load data
    train,features,stores,test= load_data()
    # standaridize column name in lower case to avoid key errors

    for df in [train,test,features,stores]:
        df.columns=[c.lower() for c in df.columns]
    # merge train with features and stores 
    train_full= train.merge(features,on=["store","date","isholiday"],how="left")
    train_full= train_full.merge(stores,on=["store"],how="left")

    # Merge test with feature and stores 

    test_full= test.merge(features,on=["store","date","isholiday"],how="left")
    test_full= test_full.merge(stores,on="store",how="left")

    # fill missing markdown (Nan-> 0)

    md_col=[c for c in train_full.columns if "markdown" in c]
    train_full[md_col]= train_full[md_col].fillna(0)
    test_full[md_col]= test_full[md_col].fillna(0)

    # fill Numeric Nan with median values 

    num_col = train_full.select_dtypes(include="number").columns
    common_cols = [c for c in num_col if c in test_full.columns]  # only fill columns that exist in both

    for c in common_cols:
        median_value = train_full[c].median()
        train_full[c] = train_full[c].fillna(median_value)
        test_full[c] = test_full[c].fillna(median_value)


    
    train_full.to_csv(OUT_DIR / "train_full.csv", index=False)
    test_full.to_csv(OUT_DIR / "test_full.csv", index=False)
    print("✅ Saved cleaned data to:", OUT_DIR)

if __name__== "__main__":
    merge_and_clean()
