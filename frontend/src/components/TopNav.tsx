"use client"
import Link from 'next/link'
import { Cloud, User } from 'lucide-react'

export default function TopNav() {
  return (
    <nav className="w-full h-20 flex items-center justify-between px-8 md:px-16 container mx-auto z-50 pt-4">
      <Link href="/" className="text-primary font-outfit text-2xl font-bold tracking-tight">
        AgriSabi
      </Link>
      
      <div className="hidden md:flex gap-8 items-center text-sm font-medium text-gray-300">
        <Link href="/dashboard" className="text-primary tracking-wide">HOME</Link>
        <Link href="#" className="hover:text-primary transition-colors tracking-wide">MARKET</Link>
        <Link href="/diagnose" className="hover:text-primary transition-colors tracking-wide">ASSISTANT</Link>
      </div>

      <div className="flex items-center gap-4 text-surface-variant">
        <button className="p-2 bg-surface-container-low rounded-full hover:bg-surface-container transition-all">
          <Cloud className="w-5 h-5 text-gray-300" />
        </button>
        <button className="p-2 border border-surface-container-high rounded-full hover:border-primary transition-all">
          <User className="w-5 h-5 text-gray-300" />
        </button>
      </div>
    </nav>
  )
}
