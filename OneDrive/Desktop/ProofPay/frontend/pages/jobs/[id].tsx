import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAppStore } from '@/store/useAppStore'
import { proofPayContract, JobData } from '@/lib/contract'

export default function JobDetail() {
  const router = useRouter()
  const { jobId } = router.query
  const { user } = useAppStore()
  const [job, setJob] = useState<JobData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (!user) {
      router.push('/login')
      return
    }

    if (jobId) {
      fetchJobDetail()
    }
  }, [jobId, user, router])

  const fetchJobDetail = async () => {
    try {
      setIsLoading(true)
      const jobData = await proofPayContract.getJob(jobId as string)
      setJob(jobData as JobData)
    } catch (error) {
      console.error('Failed to fetch job:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmitWork = async () => {
    if (!user || !jobId) return

    try {
      setIsSubmitting(true)
      // This would need the student's secret key stored securely
      // For now, this is a placeholder
      alert('Work submission functionality requires wallet integration')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleReleasePayment = async () => {
    if (!user || !jobId) return

    try {
      setIsSubmitting(true)
      // This would need the employer's secret key stored securely
      // For now, this is a placeholder
      alert('Payment release functionality requires wallet integration')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) {
    return <div className="text-center py-12">Loading job details...</div>
  }

  if (!job) {
    return <div className="text-center py-12">Job not found</div>
  }

  return (
    <div className="max-w-2xl mx-auto">
      <button
        onClick={() => router.back()}
        className="text-primary hover:text-blue-700 font-medium mb-6"
      >
        ← Back
      </button>

      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-8">
        <div className="mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{jobId}</h1>
              <p className="text-gray-600">Employer: {job.employer.slice(0, 10)}...</p>
            </div>
            <span className={`px-4 py-2 rounded-lg font-semibold ${job.completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
              {job.completed ? 'Completed' : 'In Progress'}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-8 pb-8 border-b border-slate-200">
          <div>
            <p className="text-gray-600 text-sm font-medium mb-1">Amount</p>
            <p className="text-2xl font-bold text-gray-900">{job.amount} XLM</p>
          </div>
          <div>
            <p className="text-gray-600 text-sm font-medium mb-1">Student</p>
            <p className="text-lg font-mono text-gray-900">{job.student.slice(0, 12)}...</p>
          </div>
        </div>

        {user?.role === 'student' && job.student === user.publicKey && !job.completed && (
          <button
            onClick={handleSubmitWork}
            disabled={isSubmitting}
            className="w-full px-6 py-3 bg-primary hover:bg-blue-600 disabled:bg-gray-400 text-white rounded-lg font-semibold transition-colors"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Work'}
          </button>
        )}

        {user?.role === 'employer' && job.employer === user.publicKey && job.completed && (
          <button
            onClick={handleReleasePayment}
            disabled={isSubmitting}
            className="w-full px-6 py-3 bg-secondary hover:bg-green-600 disabled:bg-gray-400 text-white rounded-lg font-semibold transition-colors"
          >
            {isSubmitting ? 'Processing...' : 'Release Payment'}
          </button>
        )}

        {job.completed && user?.role === 'employer' && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800 font-semibold">✓ Payment released</p>
          </div>
        )}
      </div>
    </div>
  )
}
