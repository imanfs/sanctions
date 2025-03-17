import pandas as pd
import regex as re
from datetime import datetime
import numpy as np

def clean_name(name_series):
    name_series = name_series.fillna('')
    
    name_series = name_series.str.lower()
    name_series = name_series.str.strip()
    name_series = name_series.str.replace(r'\s+', ' ', regex=True)
    name_series = name_series.str.replace(r'[^\w\s]', '', regex=True) # special chars
    
    return name_series

def create_full_name(row):
    names = []
    for i in range(1, 7):  # Name 1 to Name 6
        field = f'Name {i}'
        if field in row and pd.notna(row[field]) and row[field] != '':
            names.append(row[field])

    
    return ' '.join(names)

def extract_countries(country_str):
    """ Extracts country names from formatted strings like '(1) Pakistan (2) Afghanistan' """
    if pd.isna(country_str):
        return []
    
    # Handle cases like "(1) to (6) Algeria"
    country_str = re.sub(r'\(\d+\) to \(\d+\)', '', country_str)
    # Extract country names after numbers in parentheses (e.g., (1) Pakistan)
    country_str = re.sub(r'(previous address)', '', country_str)
    country_list = re.findall(r'\(\d+\)\s*([A-Za-z\s-]+)', country_str)
    country_list = [country.strip() for country in country_list]
    country_list = country_list = list(set(country_list))
    return country_list if country_list else [country_str.strip()]

def create_associated_countries(row):
    # Initialize a set to hold unique countries
    countries = set()
    
    if pd.notna(row['Country']):
        countries.add(row['Country'].strip())

    if 'Country of Birth' in row and pd.notna(row['Country of Birth']):
        extracted_countries = extract_countries(row['Country of Birth'])
        countries.update(extracted_countries)

    return list(countries)

def create_full_address(row):
    address_components = []
    for i in range(1, 7):
        field = f'Address {i}'
        if field in row and pd.notna(row[field]) and row[field] != '':
            address_components.append(str(row[field]))
    
    if 'Post/Zip Code' in row and pd.notna(row['Post/Zip Code']) and row['Post/Zip Code'] != '':
        address_components.append(str(row['Post/Zip Code']))
    
    if 'Country' in row and pd.notna(row['Country']) and row['Country'] != '':
        address_components.append(str(row['Country']))
    
    return ', '.join(address_components) if address_components else None


def find_grouped_data(x):
    unique_values = set([name for name in x if name])
    
    if len(unique_values) > 1:
        return list(unique_values)
    elif len(unique_values) == 1:
        return list(unique_values)[0]
    else:
        return None


def standardize_date(date_str):
    if pd.isna(date_str) or date_str == '':
        return None
    
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except:
        try:
            patterns = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%Y/%m/%d']
            for pattern in patterns:
                try:
                    return datetime.strptime(date_str, pattern).strftime('%Y-%m-%d')
                except:
                    pass
            
            year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
            if year_match:
                return f"{year_match.group(0)}-01-01"  # Default to January 1st
            
            return date_str  # Return as is if no pattern matched
        except:
            return date_str

def identify_duplicates(df):
    # Find exact duplicates
    exact_duplicates = df[df.duplicated(keep=False)]
    
    # Find potential duplicates based on name and DOB
    potential_duplicates = df[df.duplicated(subset=['Full_Name', 'DOB'], keep=False)]
    
    return {
        'exact_duplicates': exact_duplicates,
        'potential_duplicates': potential_duplicates
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
