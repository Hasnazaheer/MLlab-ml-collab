def missing_value_counts(df):
    """Return the number of missing values in each column."""
    return df.isnull().sum()
