import pandas as pd
import regex as re
import numpy as np

def identify_duplicates(df):
    # Find exact duplicates
    exact_duplicates = df[df.duplicated(keep=False)]
    
    # Find potential duplicates based on name and DOB
    potential_duplicates = df[df.duplicated(subset=['Global ID'], keep=False)]
    
    return {
        'exact_duplicates': exact_duplicates,
        'global_id_duplicates': potential_duplicates
    }

def assess_data_quality(df):
    # missing values
    missing_values = df.isnull().sum()
    
    # inconsistent date formats
    date_format_issues = 0
    if 'DOB' in df.columns:
        date_format_issues = df['DOB'].apply(
            lambda x: not bool(re.match(r'^\d{4}-\d{2}-\d{2}$', str(x))) if pd.notna(x) else False
        ).sum()
    
    # inconsistent name formats
    name_format_issues = df['Full_Name'].apply(lambda x: len(x) < 2 if pd.notna(x) else False).sum()
    
    missing_primary_identifiers = df.apply(
        lambda row: pd.isna(row['Full_Name']) and 
                    (pd.isna(row.get('Passport Number', np.nan)) and 
                     pd.isna(row.get('National Identification Number', np.nan))),
        axis=1
    ).sum()
    
    return {
        'missing_values': missing_values,
        'date_format_issues': date_format_issues,
        'name_format_issues': name_format_issues,
        'missing_primary_identifiers': missing_primary_identifiers
    }
