import React from 'react'
import Link from 'next/link'

interface HeaderProps {
  publicKey?: string
  onLogout?: () => void
}

export const Header: React.FC<HeaderProps> = ({ publicKey, onLogout }) => {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-green-500 rounded-lg" />
          <span className="text-xl font-bold text-gray-900">ProofPay</span>
        </Link>
        
        <nav className="hidden md:flex space-x-8">
          <Link href="/jobs" className="text-gray-700 hover:text-primary font-medium">
            Browse Jobs
          </Link>
          <Link href="/dashboard" className="text-gray-700 hover:text-primary font-medium">
            Dashboard
          </Link>
        </nav>

        <div className="flex items-center space-x-4">
          {publicKey ? (
            <>
              <span className="text-sm text-gray-600 hidden sm:inline">
                {publicKey.slice(0, 7)}...{publicKey.slice(-7)}
              </span>
              <button
                onClick={onLogout}
                className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-900 rounded-lg font-medium transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <Link href="/login" className="px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg font-medium transition-colors">
              Login
            </Link>
          )}
        </div>
      </div>
    </header>
  )
}
