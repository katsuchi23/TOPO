import pdfplumber
import pandas as pd

class PDFIngestor:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def ingest(self):
        with pdfplumber.open(self.file_path) as pdf:
            table = pdf.pages[0].extract_table()
        
        # Process table headers and data
        columns = [col.strip() for col in table[0]]  # Clean column names
        df = pd.DataFrame(table[1:], columns=columns)
        
        # Clean the data
        cleaned_data = self._clean(df.to_dict(orient='records'))
        
        return cleaned_data
    
    def _clean(self, data):
        cleaned_data = []
        
        for record in data:
            # Skip records with missing/invalid values
            if any(value in [None, 'null', 'none', 'unknown', ''] for value in record.values()):
                continue
            
            # Convert Year to integer
            try:
                record['Year'] = int(record['Year'])
            except (ValueError, KeyError):
                continue  # Skip if Year is invalid
            
            # Convert Revenue (remove commas and convert to float)
            if 'Revenue (in $)' in record:
                revenue_str = record['Revenue (in $)'].replace(',', '').strip()
                try:
                    record['Revenue (in $)'] = float(revenue_str)
                except ValueError:
                    continue  # Skip invalid revenue
            
            # Convert Memberships Sold to integer
            if 'Memberships Sold' in record:
                try:
                    # Handle potential commas or non-digit characters
                    memberships = str(record['Memberships Sold']).replace(',', '')
                    record['Memberships Sold'] = int(memberships)
                except ValueError:
                    continue  # Skip invalid memberships
            
            cleaned_data.append(record)
        
        return cleaned_data