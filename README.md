# TOPO Project

## Overview
TOPO is a full-stack application that processes and visualizes data from multiple file formats (JSON, CSV, PDF, PPTX). The system combines a Flask backend for data processing and a React frontend for visualization, providing a comprehensive solution for data integration and analysis.

## Table of Contents
- [Quick Setup](#quick-setup)
- [System Architecture](#system-architecture)
- [Backend Implementation](#backend-implementation)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Frontend Implementation](#frontend-implementation)
- [API Endpoints](#api-endpoints)
- [Data Cleaning](#data-cleaning)
- [Error Handling](#error-handling)

## Quick Setup

### Prerequisites
- Python 3.10
- Conda
- Node.js
- npm

### Backend Setup
```bash
# Create and activate conda environment
conda create -n name_environment python=3.10
conda activate name_environment

# Clone repository
git clone https://github.com/katsuchi23/TOPO.git topo
cd topo

# Install dependencies
pip install -r server/requirements.txt
conda install -c conda-forge flask pandas pytest

# Copy datasets to server directory
# Make sure datasets are in the same directory as the server

# Start backend server
cd server
python app.py
```

### Frontend Setup
```bash
# Open a new terminal
cd client
npm install # To install all dependencies
npm run dev
# Open the provided localhost URL in your browser
```

## System Architecture

### Backend Structure
```
server/
├── data_ingestion/
│   ├── __init__.py
│   ├── json_ingestor.py
│   ├── csv_ingestor.py
│   ├── pdf_ingestor.py
│   └── pptx_ingestor.py
├── app.py
└── requirements.txt
```

### Frontend Structure
```
client/
├── src/
│   └── page.tsx  
└── package.json
```

## Backend Implementation

### API Endpoints
The backend provides 5 RESTful endpoints:
1. `http://127.0.0.1:5000/api/data/pptx` - PPTX data
2. `http://127.0.0.1:5000/api/data/pdf` - PDF data
3. `http://127.0.0.1:5000/api/data/csv` - CSV data
4. `http://127.0.0.1:5000/api/data/json` - JSON data
5. `http://127.0.0.1:5000/api/data/all` - Combined data from all sources

### Data Ingestors
Each data format has a specialized ingestor class:
- `JSONIngestor`: Processes JSON company data
- `CSVIngestor`: Handles transaction records
- `PDFIngestor`: Extracts performance metrics for Company 2
- `PPTXIngestor`: Processes performance metrics for Company 1

## Data Processing Pipeline

### Data Sources
1. **JSON Dataset** (`dataset1.json`)
   - Base company information
   - Employee data
   - Primary data structure

2. **CSV Dataset** (`dataset2.csv`)
   - Transaction records
   - Activity data
   - Location information

3. **PDF Dataset** (`dataset3.pdf`)
   - Company 2 performance metrics
   - Quarterly performance data
   - Revenue information

4. **PPTX Dataset** (`dataset4.pptx`)
   - Company 1 performance metrics
   - Revenue distribution
   - Location data

### Data Combination Approach
```python
class DataProcessor:
    def __init__(self):
        self.data_sources = {
            'json': JSONIngestor('datasets/dataset1.json').ingest(),
            'csv': CSVIngestor('datasets/dataset2.csv').ingest(),
            'pdf': PDFIngestor('datasets/dataset3.pdf').ingest(),
            'pptx': PPTXIngestor('datasets/dataset4.pptx').ingest()
        }
        self.unified_data = self._merge_data()
```

The combination process involves:
1. Ingesting data from all sources
2. Cleaning and normalizing data
3. Merging based on company IDs
4. Calculating performance metrics
5. Generating annual summaries

### Transaction Processing
```python
# Split transactions by company activities
company1_activities = {'Gym', 'Pool', 'Personal Training'}
company1_transactions = [t for t in csv_data if t['Activity'] in company1_activities]
company2_transactions = [t for t in csv_data if t['Activity'] not in company1_activities]
```

## Data Cleaning

### Common Issues Handled
1. **Null Values**
```json
{
    "id": "E008",
    "name": "Jake",
    "role": "Equipment Maintenance Technician",
    "cashmoneh": 40000,
    "hired_date": null
}
```

2. **Missing Attributes**
```json
{
    "id": "E101",
    "name": "Carol",
    "role": "Spa Therapist",
    "cashmoneh": 35000
}
```

3. **Inaccurate Values**
```json
{
    "top_location": "Downtown",
    "total_memberships": 1,
    "total_revenue": 10400000.0
}
```

### Cleaning Approach
- Some values are cleaned before individual endpoint and the other after processing but before final combination
- Cross-reference validation between different data sources
- Default values provided for missing data
- Type conversion handling for consistency

### Data Combination Approach
The data combination process follows a systematic approach using the `DataProcessor` class:

#### 1. Base Structure Preparation
- Uses JSON data as the foundation for company information
- Creates a deep copy of the JSON structure to prevent data mutation
- Removes unnecessary fields like 'revenue' and 'calculated_revenue'

#### 2. Transaction Distribution
```python
# Split CSV transactions between companies
company1_activities = {'Gym', 'Pool', 'Personal Training'}
csv_data = self.data_sources['csv']
company1_transactions = [t for t in csv_data if t['Activity'] in company1_activities]
company2_transactions = [t for t in csv_data if t['Activity'] not in company1_activities]
```

#### 3. Company-Specific Processing

##### For Company 1 (ID: 1):
- Processes PPTX data for performance metrics
- Builds quarterly performance data structure:
  ```python
  company['performance'][quarter_key] = {
      'avg_duration_minutes': q.get('avg_duration_minutes', 90),
      'memberships_sold': q.get('memberships_sold', q.get('membership_sales', 0)),
      'revenue': q.get('revenue', 0.0),
      'profit_margin': q.get('profit_margin', 99.1)
  }
  ```
- Incorporates revenue distribution from PPTX
- Sets top location information
- Assigns Company 1 specific transactions

##### For Company 2 (ID: 2):
- Processes PDF data for performance metrics
- Creates performance data structure from PDF entries
- Calculates revenue distribution from transactions
- Determines top location from transaction data
- Assigns Company 2 specific transactions

#### 4. Annual Summary Calculation
The `_process_annual_summary` method:
- Groups data by year
- Processes performance data:
  - Extracts unique years from performance data
  - Calculates yearly metrics
- Analyzes transactions:
  - Filters transactions by year
  - Calculates revenue distribution
  - Determines top locations
- Generates summary statistics:
  - Total memberships and revenue
  - Revenue distribution percentages
  - Top performing locations
  - Profit margins

#### 5. Data Validation and Cleaning
- Cross-references values between different sources
- Handles missing or null values with defaults
- Validates revenue and membership numbers
- Ensures consistent data types:
  ```python
  yearly_data = {
      'year': year,
      'total_memberships': 0,
      'total_revenue': 0.0,
      'revenue_distribution': {},
      'top_location': None
  }
  ```

#### 6. Final Structure Generation
Creates a unified JSON structure with:
- Company base information
- Quarterly performance metrics
- Annual summaries
- Transaction records
- Revenue distribution
- Location data

The final output maintains consistency across both companies while preserving their unique attributes and data sources.

## Frontend Implementation

### Visualization Approach
- Single comprehensive dashboard view
- Data fetched from `/api/data/all` endpoint
- Interactive visualizations of:
  - Company performance metrics
  - Revenue distribution
  - Transaction analysis
  - Location-based insights

### Design Decisions
- Unified view instead of separate views for each data source
- Focus on combined data visualization
- Interactive elements for better data exploration

## Error Handling

### Backend Error Handling
- Safe dictionary access using `.get()`
- Default values for missing data
- Type conversion error handling
- Data validation checks

### Frontend Error Handling
- API error handling
- Loading states
- Error boundaries
- Data validation

## Output Format

### Final Data Structure Format
```json
{
  "companies": [
    {
      "annual_summary": [
        {
          "revenue_distribution": {
            "gym": 40.0,
            "personal_training": 20.0,
            "pool": 25.0,
            "tennis_court": 15.0
          },
          "top_location": "Downtown",
          "total_memberships": 1520,
          "total_revenue": 10400000.0,
          "year": 2023
        }
      ],
      "employees": [
        {
          "cashmoneh": 45000,
          "hired_date": "2020-01-15",
          "id": "E001",
          "name": "Alice",
          "role": "Personal Trainer"
        },
        {
          "cashmoneh": 62000,
          "hired_date": "2023-02-01",
          "id": "E015",
          "name": "Quinn",
          "role": "Corporate Wellness Coordinator"
        }
      ],
      "id": 1,
      "industry": "Sports and Leisure",
      "location": "North America",
      "name": "FitPro",
      "performance": {
        "2023_QQ1": {
          "avg_duration_minutes": 90,
          "memberships_sold": 320,
          "profit_margin": 99.1,
          "revenue": 2300000.0
        },
        "2023_QQ2": {
          "avg_duration_minutes": 95,
          "memberships_sold": 400,
          "profit_margin": 99.1,
          "revenue": 2500000.0
        },
        "2023_QQ3": {
          "avg_duration_minutes": 100,
          "memberships_sold": 350,
          "profit_margin": 99.1,
          "revenue": 2700000.0
        },
        "2023_QQ4": {
          "avg_duration_minutes": 92,
          "memberships_sold": 450,
          "profit_margin": 99.1,
          "revenue": 2900000.0
        }
      },
      "transactions": [
        {
          "Activity": "Gym",
          "Date": "2024-01-21",
          "Duration (Minutes)": 60,
          "Location": "Downtown",
          "Membership_ID": "M001",
          "Membership_Type": "Basic",
          "Revenue": 113.82
        },
        {
          "Activity": "Personal Training",
          "Date": "2024-01-24",
          "Duration (Minutes)": 90,
          "Location": "Westside",
          "Membership_ID": "M099",
          "Membership_Type": "VIP",
          "Revenue": 78.35
        }
      ]
    },
    {
      "annual_summary": [
        {
          "revenue_distribution": {},
          "top_location": null,
          "total_memberships": 1320,
          "total_revenue": 9600000.0,
          "year": 2022
        },
        {
          "revenue_distribution": {},
          "top_location": null,
          "total_memberships": 1520,
          "total_revenue": 10400000.0,
          "year": 2023
        },
        {
          "revenue_distribution": {},
          "top_location": null,
          "total_memberships": 920,
          "total_revenue": 6400000.0,
          "year": 2024
        }
      ],
      "employees": [
        {
          "cashmoneh": 45000,
          "hired_date": "2020-05-13",
          "id": "E103",
          "name": "Emma",
          "role": "Wellness Coach"
        },
        {
          "cashmoneh": 70000,
          "hired_date": "2023-04-15",
          "id": "E115",
          "name": "Quincy",
          "role": "Wellness Retreat Planner"
        }
      ],
      "id": 2,
      "industry": "Sports and Leisure",
      "location": "Europe",
      "name": "RecreaLife",
      "performance": {
        "2022_Q1": {
          "avg_duration_minutes": "85",
          "memberships_sold": 300,
          "profit_margin": 98.5,
          "revenue": 2100000.0
        },
        "2022_Q2": {
          "avg_duration_minutes": "87",
          "memberships_sold": 320,
          "profit_margin": 98.5,
          "revenue": 2300000.0
        },
        "2022_Q3": {
          "avg_duration_minutes": "89",
          "memberships_sold": 340,
          "profit_margin": 98.5,
          "revenue": 2500000.0
        },
        "2022_Q4": {
          "avg_duration_minutes": "88",
          "memberships_sold": 360,
          "profit_margin": 98.5,
          "revenue": 2700000.0
        },
        "2023_Q1": {
          "avg_duration_minutes": "90",
          "memberships_sold": 320,
          "profit_margin": 98.5,
          "revenue": 2300000.0
        },
        "2023_Q2": {
          "avg_duration_minutes": "95",
          "memberships_sold": 400,
          "profit_margin": 98.5,
          "revenue": 2500000.0
        },
        "2023_Q3": {
          "avg_duration_minutes": "100",
          "memberships_sold": 350,
          "profit_margin": 98.5,
          "revenue": 2700000.0
        },
        "2023_Q4": {
          "avg_duration_minutes": "92",
          "memberships_sold": 450,
          "profit_margin": 98.5,
          "revenue": 2900000.0
        },
        "2024_Q1": {
          "avg_duration_minutes": "88",
          "memberships_sold": 420,
          "profit_margin": 98.5,
          "revenue": 3100000.0
        },
        "2024_Q2": {
          "avg_duration_minutes": "90",
          "memberships_sold": 500,
          "profit_margin": 98.5,
          "revenue": 3300000.0
        }
      },
      "transactions": [
        {
          "Activity": "Dance Class",
          "Date": "2024-01-15",
          "Duration (Minutes)": 30,
          "Location": "Downtown",
          "Membership_ID": "M005",
          "Membership_Type": "VIP",
          "Revenue": 123.32
        },
        {
          "Activity": "Yoga Class",
          "Date": "2024-01-16",
          "Duration (Minutes)": 120,
          "Location": "Eastside",
          "Membership_ID": "M100",
          "Membership_Type": "Basic",
          "Revenue": 57.06
        }
      ]
    }
  ]
}
```

## Performance Considerations
- Efficient data filtering using list comprehensions
- Deep copying to prevent data mutation
- Optimized memory usage
- Selective data storage

## Testing
For running tests:
```bash
cd server
python -m pytest tests/ -v
```
This will check the ingestor function for several edge cases

## Assumptions and Challanges
1. Perfomance summary for company 2 are assumed to be the same as performance on company 1 as in the pdf dataset, it is not stated that the quarterly performance is the performance of company 1 or 2.
2. Revenue Distribution for company 2 is Null in the visualization as we are not given the dataset for that.
