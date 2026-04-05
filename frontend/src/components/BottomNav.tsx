"use client"
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Sprout, LineChart, Mic, Tractor, User as UserIcon } from 'lucide-react'

export default function BottomNav() {
  const pathname = usePathname();
  if (pathname === '/') return null; // Hide on landing page

  return (
    <div className="md:hidden fixed bottom-0 left-0 w-full h-24 bg-surface-container-lowest/80 backdrop-blur-md border-t border-surface-container/50 z-50 flex items-center justify-around px-4 pb-4">
      
      <Link href="/dashboard" className="flex flex-col items-center gap-1">
        <div className={`p-4 rounded-full transition-all duration-300 ${pathname === '/dashboard' ? 'bg-primary shadow-ambient-glow text-surface' : 'text-gray-400'}`}>
          <Sprout className="w-6 h-6" />
        </div>
        <span className="text-[10px] font-medium tracking-wide uppercase text-gray-400">Home</span>
      </Link>

      <Link href="#" className="flex flex-col items-center gap-1 text-gray-400 opacity-50">
        <div className="p-4 rounded-full">
          <LineChart className="w-6 h-6" />
        </div>
        <span className="text-[10px] font-medium tracking-wide uppercase">Market</span>
      </Link>

      <Link href="/diagnose" className="flex flex-col items-center gap-1">
        <div className={`p-4 rounded-full transition-all duration-300 ${pathname === '/diagnose' ? 'bg-primary shadow-ambient-glow text-surface' : 'text-primary'}`}>
          <Mic className="w-6 h-6" />
        </div>
        <span className="text-[10px] font-medium tracking-wide uppercase text-gray-400">AI</span>
      </Link>

      <Link href="#" className="flex flex-col items-center gap-1 text-gray-400 opacity-50">
        <div className="p-4 rounded-full">
          <Tractor className="w-6 h-6" />
        </div>
        <span className="text-[10px] font-medium tracking-wide uppercase">Yields</span>
      </Link>

      <Link href="#" className="flex flex-col items-center gap-1 text-gray-400">
        <div className="p-4 rounded-full">
          <UserIcon className="w-6 h-6" />
        </div>
        <span className="text-[10px] font-medium tracking-wide uppercase">Profile</span>
      </Link>

    </div>
  )
}
