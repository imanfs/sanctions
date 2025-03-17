from utils import *
import pandas as pd
import argparse

def process_sanctions_data(df):
    processed_df = df.copy()
    processed_df['Full_Name'] = processed_df.apply(create_full_name, axis=1)
    processed_df['Full_Name_Standardized'] = clean_name(processed_df['Full_Name'])
    processed_df["Associated Countries"] = processed_df.apply(create_associated_countries, axis=1)
    processed_df['full_address'] = processed_df.apply(create_full_address, axis=1)
    processed_df['DOB'] = processed_df['DOB'].apply(standardize_date)
    processed_df['Listed On'] = processed_df['Listed On'].apply(standardize_date)

    return processed_df

def generate_summary(df):
    df["Full_Name"] = df.apply(create_full_name, axis=1)
    quality_assessment = assess_data_quality(df)
    duplicates = identify_duplicates(df)
    
    summary = {
        'data_quality': quality_assessment,
        'duplicates': {
            'exact_duplicates': len(duplicates['exact_duplicates']),
            'potential_duplicates': len(duplicates['potential_duplicates'])
        },
        'record_count': len(df)
    }
    

    return summary

def create_final_dataset(df):
    dataset = df.groupby('Group ID').agg({
        'Full_Name': lambda x: find_grouped_data(x),
        'Country': lambda x: find_grouped_data(x),
        'Regime': lambda x: find_grouped_data(x),
        'DOB': lambda x: find_grouped_data(x),
        'Associated Countries': 'first',
        'full_address': lambda x: find_grouped_data(x),
        'Listed On': 'first',
        'Group Type': lambda x: find_grouped_data(x),
        'Last Updated': 'first'
    }).reset_index()

    # Rename the Full_Name column to Name_Variations
    dataset = dataset.rename(columns={'Full_Name': 'Name_Variations'})
    return dataset

if __name__ == "__main__":
    
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Process sanctions data.')
        parser.add_argument('--input', type=str, help='Path to the input CSV file',default='ConList.csv')
        parser.add_argument('--output_dataset', type=str, help='Path to save the final dataset CSV file',default='final_sanctions_dataset.csv')
        parser.add_argument('--output_summary', type=str, help='Path to save the data quality assessment CSV file',default='data_quality_assessment.csv')
        return parser.parse_args()

    args = parse_arguments()

    sanctions_data = pd.read_csv(args.input, skiprows=1)
    processed_sanctions_data = process_sanctions_data(sanctions_data)
    summary = generate_summary(sanctions_data)
    final_dataset = create_final_dataset(processed_sanctions_data)
    final_dataset.to_csv(args.output_dataset, index=False)
    print("Dataset generation completed successfully!")

    pd.DataFrame([summary]).to_csv(args.output_summary, index=False)
    print("Data quality summary saved successfully!")
    