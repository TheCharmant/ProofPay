import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { JobList } from '@/components/JobCard'
import { useAppStore } from '@/store/useAppStore'
import type { JobData } from '@/lib/contract'

export default function Jobs() {
  const router = useRouter()
  const { user, jobs, setJobs } = useAppStore()
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!user) {
      router.push('/login')
      return
    }

    // Fetch jobs from API
    fetchJobs()
  }, [user, router])

  const fetchJobs = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/jobs')
      const data = await response.json()
      setJobs(data.jobs || [])
    } catch (error) {
      console.error('Failed to fetch jobs:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-gray-600">Loading jobs...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-4xl font-bold text-gray-900">Available Jobs</h1>
        {user?.role === 'employer' && (
          <a
            href="/create-job"
            className="px-6 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
          >
            Post Job
          </a>
        )}
      </div>

      <JobList jobs={jobs} />
    </div>
  )
}
