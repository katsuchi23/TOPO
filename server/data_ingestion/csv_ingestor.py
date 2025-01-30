import pandas as pd

class CSVIngestor:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def ingest(self):
        df = pd.read_csv(self.file_path)
        return self._clean(df.to_dict(orient='records'))
    
    def _clean(self, data):
        cleaned_data = []
        
        for record in data:
            # Check if any field has null, None, or unknown values
            if any(
                value in [None, 'null', 'none', 'unknown', ''] 
                for value in record.values()
            ):
                continue  # Skip the record if it contains unwanted values
            
            # Convert string amounts to float
            if 'Revenue' in record and isinstance(record['Revenue'], str):
                try:
                    record['Revenue'] = float(record['Revenue'])
                except ValueError:
                    record['Revenue'] = 0.0  # Default to 0.0 if conversion fails
            
            cleaned_data.append(record)
        
        return cleaned_data
