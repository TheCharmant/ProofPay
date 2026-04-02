import React, { useState } from 'react'
import { useRouter } from 'next/router'
import { JobForm } from '@/components/JobForm'
import { useAppStore } from '@/store/useAppStore'
import { proofPayContract, JobData } from '@/lib/contract'

export default function CreateJob() {
  const router = useRouter()
  const { user, addJob } = useAppStore()
  const [isLoading, setIsLoading] = useState(false)

  const handleCreateJob = async (jobData: Partial<JobData>) => {
    if (!user || user.role !== 'employer') {
      throw new Error('Only employers can post jobs')
    }

    try {
      setIsLoading(true)

      // Create job on blockchain
      const txHash = await proofPayContract.createJob(
        jobData.jobId!,
        localStorage.getItem('employerSecret') || '',
        jobData.student!,
        jobData.amount!
      )

      const newJob: JobData = {
        employer: user.publicKey,
        student: jobData.student!,
        amount: jobData.amount!,
        completed: false,
        jobId: jobData.jobId,
      }

      addJob(newJob)

      router.push(`/jobs/${jobData.jobId}`)
    } catch (error) {
      console.error('Failed to create job:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  if (!user || user.role !== 'employer') {
    return (
      <div className="text-center py-12">
        <p className="text-lg text-gray-600 mb-4">Only employers can post jobs</p>
        <a href="/login" className="text-primary hover:text-blue-700 font-medium">
          Login as employer
        </a>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Post a New Job</h1>
        <p className="text-gray-600">Create a job listing and set the amount you're willing to pay</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <JobForm onSubmit={handleCreateJob} isLoading={isLoading} />

        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">How it works</h3>
            <ol className="space-y-2 text-blue-800 text-sm">
              <li className="flex gap-3">
                <span className="font-bold flex-shrink-0">1.</span>
                <span>Post a job with amount and student address</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold flex-shrink-0">2.</span>
                <span>Payment is locked in smart contract</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold flex-shrink-0">3.</span>
                <span>Student submits completed work</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold flex-shrink-0">4.</span>
                <span>You approve and release payment</span>
              </li>
            </ol>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-amber-900 mb-2">Tips</h3>
            <ul className="space-y-2 text-amber-800 text-sm">
              <li>• Use clear, descriptive job IDs</li>
              <li>• Double-check the student address</li>
              <li>• Set realistic amounts</li>
              <li>• Communicate clearly on what's expected</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
