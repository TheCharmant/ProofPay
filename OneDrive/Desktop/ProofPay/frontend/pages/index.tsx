import React from 'react'
import Link from 'next/link'
import { useAppStore } from '@/store/useAppStore'

export default function Home() {
  const { user } = useAppStore()

  return (
    <div className="min-h-screen">
      <section className="py-20">
        <div className="text-center">
          <div className="flex justify-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-green-500 rounded-2xl flex items-center justify-center">
              <span className="text-3xl font-bold text-white">PP</span>
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Secure Job Marketplace
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Connect with employers or students. Post jobs, submit work, and receive payments securely on the Stellar blockchain.
          </p>

          <div className="flex gap-4 justify-center">
            {user ? (
              <>
                <Link
                  href="/jobs"
                  className="px-8 py-3 bg-primary hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors"
                >
                  Browse Jobs
                </Link>
                <Link
                  href="/dashboard"
                  className="px-8 py-3 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded-lg font-semibold transition-colors"
                >
                  Dashboard
                </Link>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-8 py-3 bg-primary hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors"
                >
                  Get Started
                </Link>
                <a
                  href="#features"
                  className="px-8 py-3 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded-lg font-semibold transition-colors"
                >
                  Learn More
                </a>
              </>
            )}
          </div>
        </div>
      </section>

      <section id="features" className="py-20 bg-white border-t border-slate-200">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div className="text-center">
            <div className="text-4xl mb-4">🔐</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">Secure Escrow</h3>
            <p className="text-gray-600">Payments are locked until work is completed and approved</p>
          </div>

          <div className="text-center">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">Instant Payments</h3>
            <p className="text-gray-600">Blockchain-powered transactions with minimal fees</p>
          </div>

          <div className="text-center">
            <div className="text-4xl mb-4">🌍</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">Global Access</h3>
            <p className="text-gray-600">Work with anyone, anywhere in the world</p>
          </div>
        </div>
      </section>
    </div>
  )
}
