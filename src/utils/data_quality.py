import pandas as pd
import regex as re

def identify_duplicates(df):
    # Find exact duplicates
    exact_duplicates = df[df.duplicated(keep=False)]
    
    # Find potential duplicates based on name and DOB
    group_id_duplicates = df[df.duplicated(subset=['Group ID'], keep=False)]['Group ID'].unique()
    group_id_duplicate_rows = df[df.duplicated(subset=['Group ID'], keep=False)]
    
    return {
        'exact_duplicates': exact_duplicates,
        'group_id_duplicates': group_id_duplicates,
        'group_id_duplicate_rows': group_id_duplicate_rows
    }

def assess_data_quality(df,grouped_df):
    # missing values
    missing_values = df.isnull().sum()
    
    # inconsistent date formats
    date_format_issues = 0
    if 'DOB' in df.columns:
        date_format_issues = df['DOB'].apply(
            lambda x: not bool(re.match(r'^\d{4}-\d{2}-\d{2}$', str(x))) if pd.notna(x) else False
        ).sum()
    
    # inconsistent name formats
    n_name_variations = 0
    mean_name_variations = 0
    if 'Name Variations' in grouped_df.columns:
        n_name_variations = grouped_df['Name Variations'].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        ).sum()
        mean_name_variations = grouped_df['Name Variations'].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        ).sum() / len(grouped_df)
        
    return {
        'missing_values': missing_values.to_dict(),
        'date_format_issues': int(date_format_issues),
        'n_name_variations': int(n_name_variations),
        'mean_name_variations': mean_name_variations
    }
