import json
from typing import Dict, List

class JSONIngestor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def ingest(self) -> Dict:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return self._clean(data)
    
    def _clean(self, data: Dict) -> Dict:
        for company in data.get('companies', []):
            company['employees'] = self._clean_employees(company.get('employees', []))
            self._recalculate_company_metrics(company)
        return data
    
    def _clean_employees(self, employees: List[Dict]) -> List[Dict]:
        cleaned_employees = []
        required_keys = {"cashmoneh", "hired_date", "id", "name", "role"}
        
        for employee in employees:
            # Check if all required keys are present
            if not required_keys.issubset(employee.keys()):
                continue
            
            # Create a cleaned employee with defaults for None values
            cleaned_employee = {
                'id': employee['id'],
                'name': employee['name'],
                'role': employee['role'],
                'cashmoneh': employee['cashmoneh'] if employee['cashmoneh'] is not None else 0,
                'hired_date': employee['hired_date'] if employee['hired_date'] is not None else 'Unknown'
            }
            cleaned_employees.append(cleaned_employee)
                
        return cleaned_employees
    
    def _recalculate_company_metrics(self, company: Dict) -> None:
        if company.get('revenue') is None:
            company['revenue'] = 0
        
        total_payroll = sum(emp.get('cashmoneh', 0) for emp in company.get('employees', []))
        
        for quarter, data in company.get('performance', {}).items():
            quarter_revenue = data.get('revenue', 0) or 0
            quarterly_payroll = total_payroll / 4
            profit = quarter_revenue - quarterly_payroll
            
            profit_margin = round((profit / quarter_revenue) * 100, 1) if quarter_revenue > 0 else 0.0
            
            data['revenue'] = quarter_revenue
            data['profit_margin'] = profit_margin