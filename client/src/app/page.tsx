"use client"
import { useEffect, useState } from 'react'
import { Line, Bar, Pie } from 'react-chartjs-2'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

interface CompanyData {
  companies: {
    id: number
    name: string
    annual_summary: Array<{
      year: number
      total_revenue: number
      revenue_distribution: Record<string, number>
    }>
    performance: Record<string, {
      revenue: number
      memberships_sold: number
    }>
    employees: Array<{
      id: string
      name: string
      role: string
      cashmoneh: number
    }>
    transactions: Array<{
      Activity: string
      Revenue: number
      Date: string
      Membership_Type: string
    }>
  }[]
}

const transactionFilters = [
  { key: 'Activity', label: 'Activity' },
  { key: 'Membership_Type', label: 'Membership Type' }
]

export default function Dashboard() {
  const [data, setData] = useState<CompanyData | null>(null)
  const [selectedCompany, setSelectedCompany] = useState<number>(1)
  const [filters, setFilters] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/data/all')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch data')
        return res.json()
      })
      .then(data => {
        setData(data)
        setError('')
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-4 text-center">Loading...</div>
  if (error) return <div className="p-4 text-center text-red-500">{error}</div>
  if (!data) return <div className="p-4 text-center">No data available</div>

  const company = data.companies.find(c => c.id === selectedCompany)!

  // Filter and sort transactions
  const getUniqueValues = (key: 'Activity' | 'Membership_Type') => {
    const unique = new Set<string>()
    company.transactions.forEach(t => unique.add(t[key]))
    return Array.from(unique).sort()
  }

  const filteredTransactions = company.transactions.filter(transaction => {
    return Object.entries(filters).every(([key, value]) => {
      if (!value) return true
      const transactionValue = transaction[key as keyof typeof transaction]
      return String(transactionValue) === value
    })
  })

  const sortedTransactions = [...filteredTransactions].sort((a, b) => 
    new Date(b.Date).getTime() - new Date(a.Date).getTime()
  )

  // Revenue Trend Chart
  const allYears = Array.from(new Set(
    data.companies.flatMap(c => c.annual_summary.map(as => as.year))
  )).sort((a, b) => a - b)

  const revenueData = {
    labels: allYears,
    datasets: data.companies.map(c => ({
      label: c.name,
      data: allYears.map(year => 
        c.annual_summary.find(as => as.year === year)?.total_revenue || null
      ),
      borderColor: c.id === 1 ? '#3b82f6' : '#10b981',
    }))
  }

  // Quarterly Performance
  const quarterKeys = Object.keys(company.performance)
  const quarterlyData = {
    labels: quarterKeys,
    datasets: [
      {
        label: 'Revenue',
        data: quarterKeys.map(k => company.performance[k].revenue),
        backgroundColor: '#3b82f6',
      },
      {
        label: 'Memberships Sold',
        data: quarterKeys.map(k => company.performance[k].memberships_sold),
        backgroundColor: '#10b981',
      }
    ]
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen"> 
      <div className="mb-6">
        <select 
          className="p-2 rounded-lg border"
          onChange={(e) => {
            setSelectedCompany(Number(e.target.value))
            setFilters({})
          }}
        >
          {data.companies.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Revenue Trend */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Annual Revenue Comparison</h3>
          <Line data={revenueData} />
        </div>

        {/* Revenue Distribution */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Revenue Distribution</h3>
          {company.annual_summary.length > 0 && 
          Object.keys(company.annual_summary[0].revenue_distribution).length > 0 ? (
            <Pie
              data={{
                labels: Object.keys(company.annual_summary[0].revenue_distribution),
                datasets: [{
                  data: Object.values(company.annual_summary[0].revenue_distribution),
                  backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
                }]
              }}
            />
          ) : (
            <div className="text-gray-500 text-center py-8">
              No Data Available
            </div>
          )}
        </div>

        {/* Quarterly Performance */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Quarterly Performance</h3>
          <Bar data={quarterlyData} />
        </div>

        {/* Employee Table */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Employees</h3>
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left">Name</th>
                <th className="text-left">Role</th>
                <th className="text-left">Salary</th>
              </tr>
            </thead>
            <tbody>
              {company.employees.map(e => (
                <tr key={e.id}>
                  <td>{e.name}</td>
                  <td>{e.role}</td>
                  <td>${e.cashmoneh.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Transaction Table */}
        <div className="p-4 bg-white rounded-lg shadow col-span-full">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Recent Transactions - {company.name}</h3>
            <div className="flex gap-4">
              {transactionFilters.map(filter => (
                <select
                  key={filter.key}
                  className="p-2 rounded border text-sm"
                  value={filters[filter.key] || ''}
                  onChange={(e) => setFilters(prev => ({
                    ...prev,
                    [filter.key]: e.target.value || ''
                  }))}
                >
                  <option value="">All {filter.label}</option>
                  {getUniqueValues(filter.key as 'Activity' | 'Membership_Type').map((value, index) => (
                    <option key={index} value={value}>{value}</option>
                  ))}
                </select>
              ))}
            </div>
          </div>
          
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left p-2">Activity</th>
                <th className="text-left p-2">Date</th>
                <th className="text-left p-2">Revenue</th>
                <th className="text-left p-2">Membership Type</th>
              </tr>
            </thead>
            <tbody>
              {sortedTransactions.map((t, i) => (
                <tr key={i} className="hover:bg-gray-50">
                  <td className="p-2">{t.Activity}</td>
                  <td className="p-2">{new Date(t.Date).toLocaleDateString()}</td>
                  <td className="p-2">${t.Revenue.toFixed(2)}</td>
                  <td className="p-2">{t.Membership_Type}</td>
                </tr>
              ))}
              {sortedTransactions.length === 0 && (
                <tr>
                  <td colSpan={4} className="text-center p-4 text-gray-500">
                    No transactions found matching current filters
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}