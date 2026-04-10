"use client"
import Link from 'next/link'
import { Sun, Leaf, ArrowRight, TrendingUp, Mic, Camera } from 'lucide-react'

export default function Dashboard() {
  return (
    <div className="w-full max-w-7xl mx-auto px-4 md:px-8 pt-8 pb-32">
      
      {/* Header Info */}
      <div className="flex items-center gap-4 mb-10">
        <div className="flex items-center gap-2 bg-surface-container-low border border-surface-container-high rounded-full px-4 py-2">
           <Sun className="w-4 h-4 text-secondary" />
           <span className="text-sm font-bold bg-clip-text text-transparent bg-gradient-to-r from-on_surface to-gray-400">28°C <span className="font-medium text-xs ml-1 tracking-wider uppercase">Sunny</span></span>
        </div>
      </div>

      {/* Marquee Simulator */}
      <div className="flex gap-8 overflow-hidden whitespace-nowrap mb-12 text-xs font-bold tracking-widest uppercase">
          <div className="flex gap-2 items-center text-gray-400"><span className="text-gray-500">CASSAVA</span> <span className="text-primary">STABLE —</span></div>
          <div className="flex gap-2 items-center text-gray-400"><span className="text-gray-500">COCOA</span> <span className="text-secondary">+5% ↗</span></div>
          <div className="flex gap-2 items-center text-gray-400"><span className="text-gray-500">MAIZE</span> <span className="text-secondary">+2% ↗</span></div>
          <div className="flex gap-2 items-center text-gray-400"><span className="text-gray-500">CASSAVA</span> <span className="text-primary">STABLE —</span></div>
          <div className="flex gap-2 items-center text-gray-400"><span className="text-gray-500">COCOA</span> <span className="text-secondary">+5% ↗</span></div>
      </div>

      <div className="mb-12">
        <h1 className="font-outfit text-5xl md:text-6xl font-black text-on_surface tracking-tight mb-4">
          Harvest <span className="text-primary">Intelligence</span>
        </h1>
        <p className="text-gray-400 max-w-xl text-lg relative z-10">
          Precision insights for your acreage. Your crops are breathing; we help you hear them.
        </p>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[minmax(180px,auto)]">
        
        {/* Metric 1 */}
        <div className="md:col-span-1 md:row-span-2 bg-surface-container-low rounded-[2rem] p-8 border border-surface-container-high flex flex-col justify-between relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-full h-full bg-glass-shimmer opacity-0 group-hover:opacity-10 transition-opacity pointer-events-none" />
            <div>
              <div className="flex justify-between items-start mb-6">
                <div className="w-12 h-12 rounded-xl bg-surface-container flex items-center justify-center">
                  <Leaf className="w-6 h-6 text-primary" />
                </div>
                <div className="px-3 py-1 bg-surface-variant/40 backdrop-blur-md rounded-full text-[10px] font-bold text-gray-300 tracking-wider">
                  OPTIMAL
                </div>
              </div>
              <h3 className="font-outfit text-2xl font-bold mb-2">Corn Sector 4G</h3>
              <p className="text-sm text-gray-400 leading-relaxed mb-12">
                Hydration levels are peaking. Nutrient absorption index increased by 12% following Monday's fertilization cycle.
              </p>
            </div>
            
            <div className="flex items-end justify-between mt-auto">
              <div>
                <div className="text-4xl font-extrabold text-primary mb-1">94%</div>
                <div className="text-[10px] font-bold tracking-widest text-gray-500 uppercase">Vitality Score</div>
              </div>
              <Link href="/chat" className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center hover:bg-surface-variant transition-colors">
                 <ArrowRight className="w-4 h-4 text-gray-300" />
              </Link>
            </div>
        </div>

        {/* Hero Card */}
        <div className="md:col-span-1 md:row-span-3 bg-surface-container rounded-[2rem] border border-surface-container flex flex-col relative overflow-hidden h-[500px] md:h-auto">
           {/* Fallback pattern since we don't have the explicit image */}
           <div className="absolute inset-0 bg-gradient-to-t from-surface-container-lowest via-surface-container-lowest/80 to-transparent z-10" />
           <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1599940824399-b87987ceb72a?q=80&w=600&auto=format&fit=crop')] bg-cover bg-center mix-blend-overlay opacity-40 grayscale" />
           <div className="absolute top-[-20%] left-[-20%] w-[150%] h-[150%] bg-primary/20 blur-[100px] pointer-events-none mix-blend-color-dodge opacity-50" />
           
           <div className="p-8 mt-auto z-20 relative">
             <div className="text-[10px] font-bold tracking-widest text-secondary mb-3 uppercase">Expert Strategy</div>
             <h3 className="font-outfit text-3xl font-bold mb-4 leading-tight shadow-sm text-on_surface">Intercropping: The<br/>Symbiotic Advantage</h3>
             <p className="text-sm text-gray-300/80 leading-relaxed">
               Planting legumes alongside maize can fix nitrogen in the soil naturally, reducing synthetic fertilizer costs by up to 25%.
             </p>
           </div>
        </div>

        {/* Scan Summary */}
        <div className="md:col-span-1 bg-surface-container-low rounded-[2rem] p-6 border border-surface-container-high flex gap-4 items-center">
            <div className="w-20 h-20 rounded-xl bg-surface-variant/20 border border-surface-variant/40 flex-shrink-0 relative overflow-hidden flex items-center justify-center p-2">
               <div className="w-full h-full border border-gray-600/50 rounded-lg flex items-center justify-center opacity-40">
                  <div className="w-8 h-px bg-gray-500" />
               </div>
            </div>
            <div className="flex-1">
               <div className="text-[10px] font-bold text-gray-500 tracking-wider">SCAN #882</div>
               <h4 className="font-outfit text-lg font-bold">Early Rust Detected</h4>
               <div className="mt-3 space-y-2">
                 <div className="flex justify-between items-center text-xs bg-surface-container px-3 py-1.5 rounded-lg border border-white/5">
                   <span className="text-gray-400">Confidence</span>
                   <span className="font-bold text-secondary">82%</span>
                 </div>
                 <div className="flex justify-between items-center text-xs bg-surface-container px-3 py-1.5 rounded-lg border border-white/5">
                   <span className="text-gray-400">Spread Risk</span>
                   <span className="font-bold text-red-400">Low</span>
                 </div>
               </div>
               <div className="mt-3 text-[10px] font-bold text-primary flex items-center gap-1 cursor-pointer hover:underline uppercase tracking-wider">
                 View Protocol <ArrowRight className="w-3 h-3" />
               </div>
            </div>
        </div>

        {/* Estimated Yield */}
        <div className="md:col-span-1 bg-primary-container/20 rounded-[2rem] p-8 border border-primary/20 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 right-0 p-6">
               <div className="px-3 py-1 bg-primary-container backdrop-blur-md rounded-full text-[10px] font-bold text-primary tracking-wider">
                 PROJECTED
               </div>
            </div>
            <TrendingUp className="w-8 h-8 text-primary mb-4" />
            <h4 className="font-outfit text-xl font-bold mb-1">Estimated Yield</h4>
            <p className="text-xs text-gray-400 mb-6">Based on current biomass and climate trends.</p>
            <div className="mt-auto flex items-end gap-2">
               <span className="text-5xl font-black text-primary">4.2</span>
               <span className="text-sm font-bold text-gray-400 mb-1">Tons / HA</span>
            </div>
        </div>

        {/* Assistant Block */}
        <div className="md:col-span-1 bg-surface-container-low rounded-[2rem] p-8 border border-surface-container-high relative overflow-hidden flex flex-col items-center justify-center text-center group">
             <div className="absolute inset-0 bg-primary/5 group-hover:bg-primary/10 transition-colors pointer-events-none" />
             <Link href="/assistant" className="flex flex-col items-center group/mic z-10 transition-transform hover:scale-105">
               <div className="w-16 h-16 rounded-3xl bg-surface-container flex items-center justify-center mb-4 shadow-inner group-hover/mic:bg-surface-variant">
                   <Mic className="w-8 h-8 text-primary" />
               </div>
               <h4 className="font-outfit text-xl font-bold mb-2">Ask the Assistant</h4>
               <p className="text-xs text-gray-400 mb-6 italic">"How much water does my cassava need this week?"</p>
             </Link>
             <Link href="/diagnose" className="absolute bottom-6 right-6 w-12 h-12 bg-primary rounded-full flex items-center justify-center shadow-ambient-glow cursor-pointer hover:scale-110 transition-transform z-20">
               <Camera className="w-5 h-5 text-surface-container-lowest" />
             </Link>
        </div>

      </div>

    </div>
  )
}
