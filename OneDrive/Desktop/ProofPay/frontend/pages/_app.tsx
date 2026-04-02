import React from 'react'
import type { AppProps } from 'next/app'
import { Header } from '@/components/Header'
import { useAppStore } from '@/store/useAppStore'
import '@/styles/globals.css'

export default function App({ Component, pageProps }: AppProps) {
  const { user, logout } = useAppStore()

  return (
    <div className="min-h-screen bg-slate-50">
      <Header publicKey={user?.publicKey} onLogout={logout} />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Component {...pageProps} />
      </main>
    </div>
  )
}
