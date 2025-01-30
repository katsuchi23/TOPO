from data_ingestion import JSONIngestor, CSVIngestor, PDFIngestor, PPTXIngestor
from copy import deepcopy

class DataProcessor:
    def __init__(self):
        self.data_sources = {
            'json': JSONIngestor('datasets/dataset1.json').ingest(),
            'csv': CSVIngestor('datasets/dataset2.csv').ingest(),
            'pdf': PDFIngestor('datasets/dataset3.pdf').ingest(),
            'pptx': PPTXIngestor('datasets/dataset4.pptx').ingest()
        }
        self.unified_data = self._merge_data()

    def _process_annual_summary(self, company):
        annual_summaries = []
        performance = company.get('performance', {})
        
        # Extract unique years from performance data
        years = {int(q.split('_')[0]) for q in performance.keys()}
        
        for year in sorted(years):
            yearly_data = {
                'year': year,
                'total_memberships': 0,
                'total_revenue': 0.0,
                'revenue_distribution': {},
                'top_location': None
            }
            
            # Process performance data
            location_counts = {}
            activity_revenues = {}
            
            # Filter transactions for current year
            yearly_transactions = [
                t for t in company['transactions'] 
                if t['Date'].startswith(str(year))
            ] if company.get('transactions') else []
            
            # Calculate metrics from performance data
            for q_key, q_value in performance.items():
                q_year = int(q_key.split('_')[0])
                if q_year == year:
                    # Use correct key names based on data source
                    memberships = q_value.get('memberships_sold') or q_value.get('Memberships Sold') or 0
                    revenue = q_value.get('revenue') or q_value.get('Revenue (in $)') or 0.0
                    
                    yearly_data['total_memberships'] += int(memberships)
                    yearly_data['total_revenue'] += float(revenue)
            
            # Calculate revenue distribution and top location from transactions
            for transaction in yearly_transactions:
                activity = transaction['Activity'].lower().replace(' ', '_')
                location = transaction['Location']
                
                # Update activity revenues
                activity_revenues[activity] = activity_revenues.get(activity, 0) + transaction['Revenue']
                
                # Update location counts
                location_counts[location] = location_counts.get(location, 0) + 1
            
            # Calculate revenue distribution percentages
            if activity_revenues:
                total_activity_revenue = sum(activity_revenues.values())
                yearly_data['revenue_distribution'] = {
                    activity: round((revenue / total_activity_revenue) * 100, 1)
                    for activity, revenue in activity_revenues.items()
                }
            
            # Determine top location
            if location_counts:
                yearly_data['top_location'] = max(location_counts, key=location_counts.get)
            
            annual_summaries.append(yearly_data)
        
        return annual_summaries


    def _merge_data(self):
        # Split CSV transactions
        company1_activities = {'Gym', 'Pool', 'Personal Training'}
        csv_data = self.data_sources['csv']
        company1_transactions = [t for t in csv_data if t['Activity'] in company1_activities]
        company2_transactions = [t for t in csv_data if t['Activity'] not in company1_activities]

        # Process companies
        json_data = deepcopy(self.data_sources['json'])
        companies = json_data['companies']
        pptx_data = self.data_sources['pptx']
        pdf_data = self.data_sources['pdf']
        
        for company in companies:
            # Clean up existing fields
            for field in ['revenue', 'calculated_revenue']:
                company.pop(field, None)

            if company['id'] == 1:
                # Process PPTX data
                pptx_revenue_dist = pptx_data.get('revenue_distribution', {})
                pptx_top_location = pptx_data.get('top_location', 'Downtown')
                
                # Build performance metrics
                company['performance'] = {}
                for q in pptx_data.get('quarterly_metrics', []):
                    year = 2023
                    quarter_key = f"{year}_Q{q.get('quarter', 1)}"
                    company['performance'][quarter_key] = {
                        'avg_duration_minutes': q.get('avg_duration_minutes', 90),
                        'memberships_sold': q.get('memberships_sold', q.get('membership_sales', 0)),
                        'revenue': q.get('revenue', 0.0),
                        'profit_margin': q.get('profit_margin', 99.1)
                    }
                
                # Process annual summary with PPTX data
                annual_summary = self._process_annual_summary(company)
                for summary in annual_summary:
                    summary['revenue_distribution'] = pptx_revenue_dist.copy()
                    summary['top_location'] = pptx_top_location
                
                company['annual_summary'] = annual_summary
                company['transactions'] = company1_transactions
                
            elif company['id'] == 2:
                # Process PDF data
                company['performance'] = {}
                for entry in pdf_data:
                    year = entry.get('Year', 2022)
                    quarter = entry.get('Quarter', 'Q1')
                    quarter_key = f"{year}_{quarter}"
                    company['performance'][quarter_key] = {
                        'avg_duration_minutes': entry.get('Avg Duration (Minutes)', 90),
                        'memberships_sold': entry.get('Memberships Sold', 0),
                        'revenue': entry.get('Revenue (in $)', 0.0),
                        'profit_margin': entry.get('profit_margin', 98.5)
                    }
                
                company['annual_summary'] = self._process_annual_summary(company)
                company['transactions'] = company2_transactions

        return {'companies': companies}

    def get_data_by_type(self, file_type):
        return self.data_sources.get(file_type.lower(), {})

    