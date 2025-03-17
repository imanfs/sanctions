# Sanctions Data Processor

A Python-based tool for processing, cleaning, and analyzing sanctions data from various sources.

## Overview

This project provides a comprehensive data processing pipeline for sanctions data. It standardizes names, addresses, and dates, identifies duplicates, assesses data quality, and generates a clean, consolidated dataset ready for further analysis.

## Usage Instructions

```python
# Process sanctions data
python generate_dataset.py --input ConList.csv --output_dataset final_sanctions_dataset.csv --output_summary data_quality_assessment.csv
```

## Features

- **Data Standardization**
  - Name normalization and full name creation
  - Address consolidation
  - Date format standardization
  - Country extraction and normalization

- **Quality Assessment**
  - Missing value detection
  - Date format validation
  - Name format validation
  - Primary identifier validation

- **Duplicate Detection**
  - Exact duplicate identification
  - Potential duplicate identification based on name and date of birth

- **Group-Based Consolidation**
  - Consolidates entries by Group ID
  - Handles multiple variations of names, countries, and other fields

## Data Quality Insights

From the latest run:
- **Record Count**: 18,765 entries
- **Duplicates**: 
  - 107 exact duplicates
  - 6,043 potential duplicates

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

