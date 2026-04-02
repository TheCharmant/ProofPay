import React, { useEffect } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import { useAppStore } from '@/store/useAppStore'

export default function Dashboard() {
  const router = useRouter()
  const { user, jobs } = useAppStore()

  useEffect(() => {
    if (!user) {
      router.push('/login')
    }
  }, [user, router])

  if (!user) {
    return null
  }

  const myJobs = jobs.filter(
    (job) => job.employer === user.publicKey || job.student === user.publicKey
  )

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back, {user.role === 'employer' ? 'Employer' : 'Student'}!</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <p className="text-gray-600 text-sm font-medium mb-2">Your Address</p>
          <p className="font-mono text-lg font-bold break-all">{user.publicKey.slice(0, 20)}...</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <p className="text-gray-600 text-sm font-medium mb-2">Role</p>
          <p className="text-lg font-bold capitalize">{user.role}</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <p className="text-gray-600 text-sm font-medium mb-2">My Jobs</p>
          <p className="text-lg font-bold">{myJobs.length}</p>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Jobs</h2>

        {myJobs.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-8 text-center">
            <p className="text-gray-600 mb-4">No jobs yet</p>
            <div className="flex gap-4 justify-center">
              {user.role === 'employer' && (
                <Link
                  href="/create-job"
                  className="px-6 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-600"
                >
                  Post First Job
                </Link>
              )}
              <Link
                href="/jobs"
                className="px-6 py-2 bg-gray-200 text-gray-900 rounded-lg font-medium hover:bg-gray-300"
              >
                Browse Jobs
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {myJobs.map((job) => (
              <Link key={job.jobId} href={`/jobs/${job.jobId}`}>
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow cursor-pointer">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">{job.jobId}</h3>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        job.completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {job.completed ? 'Completed' : 'In Progress'}
                    </span>
                  </div>
                  <p className="text-gray-700 mb-4">
                    <span className="font-semibold">{job.amount} XLM</span>
                  </p>
                  <div className="text-sm text-gray-600">
                    {job.employer === user.publicKey ? (
                      <p>You are the employer</p>
                    ) : (
                      <p>You are the student</p>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      <Link
        href="/jobs"
        className="inline-block px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded-lg font-medium transition-colors"
      >
        Browse More Jobs
      </Link>
    </div>
  )
}
