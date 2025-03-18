from utils.data_processing import *
from utils.data_quality import *
import pandas as pd
import argparse
import json

def process_sanctions_data(df):
    processed_df = df.copy()

    processed_df['Full Name'] = processed_df.apply(create_full_name, axis=1)
    processed_df['Full Name'] = processed_df['Full Name'].apply(clean_name)

    processed_df['Primary Name'] = processed_df.apply(lambda row: row['Full Name'] if row['Alias Type'] == 'Primary name' else None, axis=1)
    processed_df['Name Variations'] = processed_df.apply(lambda row: row['Full Name'] if row['Alias Type'] != 'Primary name' else None, axis=1)
    
    processed_df["Associated Countries"] = processed_df.apply(create_associated_countries, axis=1)
    processed_df['Full Address'] = processed_df.apply(create_full_address, axis=1)
    processed_df['Standardised Date of Birth'] = processed_df['DOB'].apply(standardize_date)
    processed_df['Listed On'] = processed_df['Listed On'].apply(standardize_date)

    return processed_df

def group_sanctions_data(df):
    dataset = df.groupby('Group ID').agg({
        'Primary Name': lambda x: find_grouped_data(x),
        'Name Variations': lambda x: find_grouped_data(x),
        'Country': lambda x: find_grouped_data(x),
        'Regime': lambda x: find_grouped_data(x),
        'Standardised Date of Birth': lambda x: find_grouped_data(x),
        'Associated Countries': 'first',
        'Full Address': lambda x: find_grouped_data(x),
        'Listed On': 'first',
        'Group Type': lambda x: find_grouped_data(x),
        'Last Updated': 'first'
    }).reset_index()

    return dataset

def generate_summary(df,processed_df):
    quality_assessment = assess_data_quality(df,processed_df)
    duplicates = identify_duplicates(df)
    
    summary = {
        'data_quality': quality_assessment,
        'duplicates': {
            'exact_duplicates': len(duplicates['exact_duplicates']),
            'group_id_duplicates': len(duplicates['group_id_duplicates']),
            'group_id_duplicate_rows': len(duplicates['group_id_duplicate_rows'])
        },
        'record_count': len(df),
        'processed_entries': len(processed_df)
    }
    
    return summary

if __name__ == "__main__":
    
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Process sanctions data.')
        parser.add_argument('--input', type=str, help='Path to the input CSV file',default='data/ConList.csv')
        parser.add_argument('--output_dataset', type=str, help='Path to save the final dataset CSV file',default='data/outputs/sanctions_dataset.csv')
        parser.add_argument('--output_summary', type=str, help='Path to save the data quality assessment CSV file',default='data/outputs/data_quality_assessment.json')
        return parser.parse_args()

    args = parse_arguments()

    sanctions_data = pd.read_csv(args.input, skiprows=1)
    
    processed_sanctions_data = process_sanctions_data(sanctions_data)
    grouped_sanctions_data = group_sanctions_data(processed_sanctions_data)
    grouped_sanctions_data.to_csv(args.output_dataset, index=False)
    
    print(f"Structured dataset saved successfully to {args.output_dataset}!")

    summary = generate_summary(sanctions_data,grouped_sanctions_data)
    with open(args.output_summary, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"Data quality summary saved successfully to {args.output_summary}!")
    