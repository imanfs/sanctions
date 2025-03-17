from utils import *
import pandas as pd

def process_sanctions_data(df):
    processed_df = df.copy()
    print(processed_df.columns)
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
    sanctions_data = pd.read_csv('ConList.csv',skiprows=1)
    processed_sanctions_data = process_sanctions_data(sanctions_data)
    summary = generate_summary(sanctions_data)
    final_dataset = create_final_dataset(processed_sanctions_data)
    
    # Save the final dataset to a CSV file
    final_dataset.to_csv('final_sanctions_dataset.csv', index=False)
    
    # Save the data quality assessment to a CSV file
    pd.DataFrame([summary]).to_csv('data_quality_assessment.csv', index=False)
    
