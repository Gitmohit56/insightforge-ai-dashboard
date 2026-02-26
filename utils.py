import pandas as pd

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(0)
    return df

def get_summary(df):
    return df.describe().to_string()