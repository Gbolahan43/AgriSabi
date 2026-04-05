"use client"
import Link from 'next/link'
import { ArrowRight, Leaf, Mic, LineChart, FlaskConical, Target } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen relative flex flex-col items-center">
      {/* Background Gradients acting as light diffusers */}
      <div className="absolute top-[-10%] left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-primary/20 rounded-full blur-[120px] pointer-events-none -z-10" />

      {/* HERO SECTION */}
      <section className="w-full max-w-6xl mx-auto px-6 pt-24 pb-32 flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-surface-container-low border border-surface-container-high/50 mb-8 backdrop-blur-md">
          <Leaf className="w-4 h-4 text-primary" />
          <span className="text-xs font-semibold tracking-wider uppercase text-gray-300">Empowering African Agriculture</span>
        </div>

        <h1 className="font-outfit text-5xl md:text-7xl font-extrabold tracking-tight text-on_surface leading-[1.1] mb-6 max-w-4xl">
          Bridging the Gap<br className="hidden md:block"/> Between <span className="text-primary bg-clip-text">Research</span><br className="hidden md:block"/> and the <span className="text-secondary italic">African Farmer</span>.
        </h1>

        <p className="text-lg md:text-xl text-gray-400 max-w-2xl mb-10 leading-relaxed font-light">
          Transforming complex agricultural data into actionable soil-to-market insights through voice, vision, and AI.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-6">
          <Link href="/diagnose" className="group px-8 py-4 rounded-3xl bg-primary-glow shadow-ambient-glow text-surface font-semibold flex items-center gap-2 hover:shadow-ambient-glow-high transition-all duration-300">
            Start Diagnosing Now
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link href="/dashboard" className="px-8 py-4 rounded-3xl border border-surface-container text-on_surface font-semibold hover:bg-surface-container transition-all text-sm tracking-wide">
            View Market Insights
          </Link>
        </div>
      </section>

      {/* DASHBOARD PREVIEW MOCKUP */}
      <section className="w-full max-w-5xl mx-auto px-6 mb-32 relative">
        <div className="w-full bg-surface-container-lowest border border-surface-container rounded-[2.5rem] p-2 md:p-4 shadow-2xl relative overflow-hidden group">
          <div className="absolute inset-0 bg-glass-shimmer opacity-30 z-10 pointer-events-none group-hover:opacity-10 transition-opacity duration-1000" />
          <div className="w-full rounded-[2rem] overflow-hidden relative">
            <img src="/harvest_mockup.png" alt="Harvest Intelligence Mockup" className="w-full h-auto object-cover" />
          </div>
        </div>
      </section>

      {/* FEATURES GRID */}
      <section className="w-full max-w-6xl mx-auto px-6 pb-40">
        <div className="text-center mb-16">
          <h2 className="font-outfit text-3xl md:text-4xl font-bold text-on_surface mb-4">Precision Tools for <span className="text-primary underline decoration-primary/30 underline-offset-8">Sustainable Growth</span></h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          {/* Feature 1 */}
          <div className="bg-surface-container-low rounded-3xl p-8 border border-surface-container-high hover:border-primary/50 transition-colors flex flex-col md:flex-row gap-6 items-center">
            <div className="flex-1 space-y-4">
              <div className="w-12 h-12 rounded-full bg-surface-container flex items-center justify-center">
                <Target className="text-primary w-6 h-6" />
              </div>
              <h3 className="font-outfit text-xl font-bold text-on_surface">Instant Crop Diagnosis</h3>
              <p className="text-gray-400 text-sm leading-relaxed">Upload a photo of your crops to identify pests and diseases instantly. Powered by advanced neural networks trained on African soil profiles.</p>
              <div className="flex gap-2">
                <span className="text-[10px] font-bold bg-surface-container py-1 px-3 rounded-full text-gray-300">98% ACCURACY</span>
                <span className="text-[10px] font-bold bg-surface-container py-1 px-3 rounded-full text-gray-300">REAL-TIME</span>
              </div>
            </div>
            <div className="w-40 h-40 bg-surface-container rounded-2xl md:ml-auto shadow-inner flex items-center justify-center">
               <Leaf className="w-16 h-16 text-primary/50 blur-[2px]" />
            </div>
          </div>

          {/* Feature 2 */}
          <div className="bg-surface-container-low rounded-3xl p-8 border border-surface-container-high hover:border-secondary/50 transition-colors">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-full bg-surface-container flex items-center justify-center text-secondary">
                <Mic className="w-6 h-6" />
              </div>
              <h3 className="font-outfit text-xl font-bold text-on_surface">Live Voice Assistant</h3>
              <p className="text-gray-400 text-sm leading-relaxed">Natural language interactions in your language. Get expert clinical advice while you're physically working in the field.</p>
              <Link href="/diagnose" className="inline-flex text-secondary text-sm font-semibold mt-4 hover:underline">
                Try Voice Assist {'>'}
              </Link>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="bg-surface-container-low rounded-3xl p-8 border border-surface-container-high hover:border-primary/50 transition-colors">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-full bg-surface-container flex items-center justify-center text-primary">
                <LineChart className="w-6 h-6" />
              </div>
              <h3 className="font-outfit text-xl font-bold text-on_surface">Market Intelligence</h3>
              <p className="text-gray-400 text-sm leading-relaxed">Real-time pricing spanning local and regional markets to ensure you get the best value for your hard work.</p>
            </div>
          </div>

          {/* Feature 4 */}
          <div className="bg-surface-container-low rounded-3xl p-8 border border-surface-container-high flex flex-row gap-6 relative overflow-hidden">
            <div className="absolute inset-0 bg-primary-glow opacity-5" />
            <div className="relative z-10 flex-1 space-y-4">
              <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center text-primary backdrop-blur-md">
                <FlaskConical className="w-6 h-6" />
              </div>
              <h3 className="font-outfit text-xl font-bold text-on_surface">The Research Bridge</h3>
              <p className="text-gray-400 text-sm leading-relaxed">Access curated scientific findings from top agricultural universities globally, translated into simple local techniques.</p>
            </div>
          </div>

        </div>
      </section>

      {/* CTA SECTION */}
      <section className="w-full max-w-5xl mx-auto px-6 pb-24">
        <div className="w-full bg-primary-glow rounded-[3rem] p-12 text-center shadow-ambient-glow-high flex flex-col items-center">
            <h2 className="font-outfit text-3xl md:text-5xl font-bold text-surface mb-6">Ready to Optimize Your Harvest?</h2>
            <p className="text-surface/80 max-w-xl mx-auto mb-10 font-medium">Join 15,000+ African farmers using AgriSabi to build a more resilient and profitable agricultural future.</p>
            <Link href="/dashboard" className="px-8 py-4 rounded-3xl bg-surface text-primary font-bold hover:scale-105 transition-transform duration-300">
               Get Started for Free
            </Link>
            <p className="mt-6 text-xs text-surface/60 font-semibold tracking-wider">AVAILABLE ON WEB & MOBILE</p>
        </div>
      </section>

      <footer className="w-full border-t border-surface-container py-8 text-center text-sm text-gray-500 flex flex-col md:flex-row justify-between items-center px-12">
        <div>© 2026 AgriSabi. All rights reserved.</div>
        <div className="flex gap-4 mt-4 md:mt-0">
           <span className="hover:text-primary cursor-pointer">Privacy</span>
           <span className="hover:text-primary cursor-pointer">Terms</span>
        </div>
      </footer>
    </div>
  )
}
