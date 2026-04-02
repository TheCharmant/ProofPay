import React, { useState } from 'react'
import { useRouter } from 'next/router'
import { LoginForm } from '@/components/LoginForm'
import { useAppStore } from '@/store/useAppStore'
import { proofPayContract } from '@/lib/contract'

export default function Login() {
  const router = useRouter()
  const { setUser } = useAppStore()
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (secretKey: string, role: 'employer' | 'student') => {
    setIsLoading(true)
    try {
      proofPayContract.setKeypair(secretKey)
      const publicKey = proofPayContract.getPublicKey()

      setUser({
        publicKey,
        role,
        balance: 0,
      })

      router.push('/dashboard')
    } catch (error) {
      console.error('Login error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12">
      <LoginForm onSubmit={handleLogin} isLoading={isLoading} />
    </div>
  )
}
