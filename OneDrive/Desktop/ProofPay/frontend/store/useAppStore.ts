import { create } from 'zustand'
import { JobData } from './contract'

interface User {
  publicKey: string
  role: 'employer' | 'student' | null
  balance: number
}

interface AppStore {
  user: User | null
  jobs: JobData[]
  isLoading: boolean
  error: string | null
  
  setUser: (user: User | null) => void
  setJobs: (jobs: JobData[]) => void
  addJob: (job: JobData) => void
  setLoading: (isLoading: boolean) => void
  setError: (error: string | null) => void
  logout: () => void
}

export const useAppStore = create<AppStore>((set) => ({
  user: null,
  jobs: [],
  isLoading: false,
  error: null,
  
  setUser: (user) => set({ user }),
  setJobs: (jobs) => set({ jobs }),
  addJob: (job) => set((state) => ({ jobs: [...state.jobs, job] })),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  logout: () => set({ user: null, jobs: [] }),
}))
