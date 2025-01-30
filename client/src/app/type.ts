// types.ts
export interface Transaction {
    Activity: string;
    Date: string;
    'Duration (Minutes)': number;
    Location: string;
    Membership_ID: string;
    Membership_Type: string;
    Revenue: number;
  }
  
  export interface Employee {
    cashmoneh: number;
    hired_date: string | null;
    id: string;
    name: string;
    role: string;
  }
  
  export interface CompanyPerformance {
    profit_margin: number;
    revenue: number | null;
  }
  
  export interface Company {
    id: number;
    name: string;
    industry: string;
    location: string;
    revenue: number | null;
    employees: Employee[];
    performance: {
      [key: string]: CompanyPerformance;
    };
  }
  
  export interface QuarterlyPerformance {
    'Avg Duration (Minutes)': string;
    'Memberships Sold': number;
    Quarter: string;
    'Revenue (in $)': number;
    Year: string;
  }
  
  export interface AnnualSummary {
    total_revenue: number;
  }
  
  export interface ApiResponse {
    companies?: Company[];
    transactions?: Transaction[];
    quarterly_performance?: QuarterlyPerformance[];
    annual_summary?: AnnualSummary;
  }