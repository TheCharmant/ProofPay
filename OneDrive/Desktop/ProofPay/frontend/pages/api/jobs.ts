import type { NextApiRequest, NextApiResponse } from 'next'

interface Job {
  jobId: string
  employer: string
  student: string
  amount: number
  completed: boolean
}

// Mock database - in production, this would be real data
const mockJobs: Job[] = [
  {
    jobId: 'web-design-001',
    employer: 'GBRPYHIL2CI3WHZDTOOQFC6EB4KJJGUJMVOC2LCLUHVM4LOCJLUYY5M',
    student: 'GDZST3XVCDTUJ76ZAV2HA72KYXM4Y5L4EOYM4XVWG3IWJQPQ5YFGQG3',
    amount: 500,
    completed: false,
  },
  {
    jobId: 'content-writing-001',
    employer: 'GBRPYHIL2CI3WHZDTOOQFC6EB4KJJGUJMVOC2LCLUHVM4LOCJLUYY5M',
    student: 'GDZST3XVCDTUJ76ZAV2HA72KYXM4Y5L4EOYM4XVWG3IWJQPQ5YFGQG3',
    amount: 300,
    completed: true,
  },
]

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Get all jobs
    res.status(200).json({ jobs: mockJobs })
  } else if (req.method === 'POST') {
    // Create new job
    const { jobId, employer, student, amount } = req.body
    const newJob: Job = {
      jobId,
      employer,
      student,
      amount,
      completed: false,
    }
    mockJobs.push(newJob)
    res.status(201).json(newJob)
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
