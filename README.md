# Sanctions Data Processor

A Python-based tool for processing, cleaning, and analyzing sanctions data from the [UK Financial Sanctions list](https://www.gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets/consolidated-list-of-targets). Detailed descriptions of each field in the dataset can be found in the guide [here](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1057741/280222_Consolidated_List_Format_Guide.pdf).

## Overview

This project provides a comprehensive data processing pipeline for financial sanctions data. It standardizes names, addresses, and dates, identifies duplicates, assesses data quality in a JSON-format report, and generates a clean, consolidated dataset ready for further analysis.

## Usage Instructions

```python
# Process sanctions data
python src/main.py --input data/ConList.csv --output_dataset data/outputs/sanctions_dataset.csv --output_summary data/outputs/data_quality_assessment.json
```

## Dataset Structure

- **Data Cleaning and Prep**
  - Name cleaning
  - Address consolidation for full address
  - Date format standardization
  - Country extraction and associated countries list creation

- **Group-Based Consolidation**
  - Aggregates entries by Group ID
  - Handles multiple variations of names, countries, and dates of birth

## Data Quality Insights

### Overview  
- **Total Record Count**: 18,765 entries  
- **Processed Unique Entries**: 4,666  

### Duplicate Analysis  
- **Exact Duplicates**: 107  
- **Group ID Duplicates**:  
  - 2,499 unique `Group ID` entries have at least one duplicate  
  - Total duplicate rows associated with `Group ID` values: 16,598  
- **Name Variations**:  
  - Across 4,066 unique `Group ID` entries, there are 7,054 name variations  
  - **Average Name Variations per Entry**: ~1.51  
  - **Implications**:  
    - Name variations are critical for financial crime monitoring  
    - Fuzzy matching should be implemented to compare names against all known variations  

### Missing Data Breakdown  
Fields with the highest number of missing values:  
- **Name 5**: 18,730 missing  
- **Name 4**: 18,512 missing  
- **Title**: 17,712 missing  
- **DOB (Date of Birth)**: 6,405 missing  
- **Nationality**: 8,290 missing  
- **Passport Number**: 15,996 missing  
- **Address Fields**:  
  - Address 1: 12,288 missing  
  - Address 2: 15,253 missing  
  - Address 3: 16,782 missing  
  - Address 4: 17,998 missing  

### Date Format Issues  
- **12,360 entries** contain inconsistent or improperly formatted dates in the `DOB` field  
- **Recommendation**: Implement strict validation and normalization for date formatting  

### Key Takeaways  
1. **Data Quality Concerns**  
   - High missing value counts in key identification fields could impact entity resolution.  
   - Address completeness varies significantly, requiring enrichment strategies.  
2. **Duplicate Management**  
   - Group ID duplication suggests potential data redundancy or entity fragmentation.  
   - Entity consolidation rules should be refined to prevent duplicate persistence.  
3. **Enhanced Name Matching Needed**  
   - Name variations are prevalent and need to be accounted for in financial crime screening.  
   - Fuzzy matching should be integrated into screening algorithms.  

## Key Functions

### Data Processing
- `clean_name()`: Standardizes name formatting
- `create_full_name()`: Combines name components into a full name
- `extract_countries()`: Parses country information from formatted strings
- `create_associated_countries()`: Compiles countries associated with an individual
- `create_full_address()`: Consolidates address components
- `standardize_date()`: Normalizes date formats to YYYY-MM-DD

### Analysis
- `identify_duplicates()`: Finds exact and potential (based on full name and DOB) duplicate records
- `assess_data_quality()`: Evaluates data completeness and format consistency
- `find_grouped_data()`: Aggregates related data points

