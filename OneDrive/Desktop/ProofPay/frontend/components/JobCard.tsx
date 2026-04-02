import React from 'react'
import Link from 'next/link'
import { JobData } from '../lib/contract'

interface JobCardProps {
  job: JobData
  onClick?: () => void
}

export const JobCard: React.FC<JobCardProps> = ({ job, onClick }) => {
  const statusColor = job.completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
  const statusText = job.completed ? 'Completed' : 'In Progress'

  return (
    <div onClick={onClick} className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow cursor-pointer">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{job.jobId || 'Job'}</h3>
          <p className="text-sm text-gray-600">Posted by {job.employer.slice(0, 7)}...</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColor}`}>
          {statusText}
        </span>
      </div>

      <div className="mb-4 space-y-2">
        <p className="text-gray-700">
          <span className="font-semibold">Amount:</span> {job.amount} XLM
        </p>
        <p className="text-gray-700">
          <span className="font-semibold">Student:</span> {job.student.slice(0, 10)}...
        </p>
      </div>

      <div className="pt-4 border-t border-slate-200">
        <button className="w-full px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg font-medium transition-colors">
          View Details
        </button>
      </div>
    </div>
  )
}

export const JobList: React.FC<{ jobs: JobData[] }> = ({ jobs }) => {
  if (!jobs || jobs.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 mb-4">No jobs found</p>
        <Link href="/create-job" className="inline-block px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-600">
          Post First Job
        </Link>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {jobs.map((job) => (
        <Link key={job.jobId} href={`/jobs/${job.jobId}`}>
          <JobCard job={job} />
        </Link>
      ))}
    </div>
  )
}
