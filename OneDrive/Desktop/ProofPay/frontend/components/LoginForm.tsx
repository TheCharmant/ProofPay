import React, { useState } from 'react'

interface LoginFormProps {
  onSubmit: (secretKey: string, role: 'employer' | 'student') => Promise<void>
  isLoading?: boolean
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, isLoading = false }) => {
  const [secretKey, setSecretKey] = useState('')
  const [role, setRole] = useState<'employer' | 'student'>('employer')
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!secretKey) {
      setError('Secret key is required')
      return
    }

    if (!secretKey.startsWith('S')) {
      setError('Invalid Stellar secret key (must start with S)')
      return
    }

    try {
      await onSubmit(secretKey, role)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-slate-200 p-8 max-w-md mx-auto">
      <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome to ProofPay</h2>
      <p className="text-gray-600 mb-6">Connect your Stellar wallet to get started</p>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Your Role</label>
          <div className="flex gap-4">
            <label className="flex items-center">
              <input
                type="radio"
                value="employer"
                checked={role === 'employer'}
                onChange={(e) => setRole(e.target.value as 'employer' | 'student')}
                disabled={isLoading}
                className="mr-2"
              />
              <span className="text-gray-700">Employer</span>
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                value="student"
                checked={role === 'student'}
                onChange={(e) => setRole(e.target.value as 'employer' | 'student')}
                disabled={isLoading}
                className="mr-2"
              />
              <span className="text-gray-700">Student</span>
            </label>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Secret Key</label>
          <textarea
            value={secretKey}
            onChange={(e) => setSecretKey(e.target.value)}
            placeholder="Paste your Stellar secret key here (starts with S)"
            disabled={isLoading}
            className="w-full min-h-24 font-mono text-sm"
            required
          />
          <p className="text-xs text-gray-500 mt-2">Never share your secret key. It&apos;s only used locally.</p>
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full mt-6 px-4 py-3 bg-primary hover:bg-blue-600 disabled:bg-gray-400 text-white rounded-lg font-medium text-lg transition-colors"
      >
        {isLoading ? 'Connecting...' : 'Connect Wallet'}
      </button>
    </form>
  )
}
