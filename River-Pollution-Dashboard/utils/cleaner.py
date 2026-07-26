import pandas as pd


def clean_ganga(df):
    """
    Clean Ganga Dataset
    """

    df = df.copy()

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove missing values
    df = df.dropna()

    return df


def clean_water(df):
    """
    Clean Water Quality Dataset
    """

    df = df.copy()

    # Standardize column names
    df.columns = df.columns.str.strip()

    # Remove duplicates
    df = df.drop_duplicates()

    return df