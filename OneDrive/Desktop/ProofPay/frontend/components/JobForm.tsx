import React, { useState } from 'react'
import { JobData } from '../lib/contract'

interface JobFormProps {
  onSubmit: (data: Partial<JobData>) => Promise<void>
  isLoading?: boolean
}

export const JobForm: React.FC<JobFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState({
    jobId: '',
    studentAddress: '',
    amount: '',
  })

  const [error, setError] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!formData.jobId || !formData.studentAddress || !formData.amount) {
      setError('All fields are required')
      return
    }

    try {
      await onSubmit({
        jobId: formData.jobId,
        student: formData.studentAddress,
        amount: parseInt(formData.amount, 10),
      })

      setFormData({ jobId: '', studentAddress: '', amount: '' })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 max-w-md">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Post a New Job</h2>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Job ID</label>
          <input
            type="text"
            name="jobId"
            value={formData.jobId}
            onChange={handleChange}
            placeholder="e.g., job-001"
            disabled={isLoading}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Student Address</label>
          <input
            type="text"
            name="studentAddress"
            value={formData.studentAddress}
            onChange={handleChange}
            placeholder="Stellar address"
            disabled={isLoading}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Amount (XLM)</label>
          <input
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            placeholder="e.g., 100"
            min="1"
            disabled={isLoading}
            required
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full mt-6 px-4 py-2 bg-primary hover:bg-blue-600 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
      >
        {isLoading ? 'Creating...' : 'Create Job'}
      </button>
    </form>
  )
}
