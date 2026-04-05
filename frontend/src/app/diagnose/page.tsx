"use client"
import { useState, useRef } from 'react'
import { Camera, ChevronDown, FlaskConical, Leaf, AlertTriangle, ShieldCheck, Loader2 } from 'lucide-react'
import { uploadForDiagnosis, DiagnosisResponse } from '@/lib/api'

export default function DiagnosePage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DiagnosisResponse | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;

    setFile(selected);
    const objectUrl = URL.createObjectURL(selected);
    setPreview(objectUrl);
    setError(null);
    setResult(null);

    // Auto-fire Analysis
    setIsLoading(true);
    try {
      const data = await uploadForDiagnosis(selected);
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to connect to AI core.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto px-4 md:px-8 pt-8 pb-32">
      
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="font-outfit text-4xl md:text-5xl font-bold tracking-tight mb-4 text-on_surface">AI Crop Diagnosis</h1>
        <p className="text-gray-400 text-sm max-w-xl mx-auto">
          Upload a clear photo of your affected crop to receive instant biological insights and treatment recommendations.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-8 mb-16">
        
        {/* Upload Region */}
        <div 
           onClick={() => fileInputRef.current?.click()}
           className={`md:col-span-3 bg-surface-container-lowest border-2 border-dashed ${error ? 'border-red-500/50' : 'border-surface-container-high hover:border-primary/50'} hover:bg-surface-container-low transition-all duration-500 rounded-[3rem] min-h-[400px] flex flex-col items-center justify-center p-8 group cursor-pointer relative overflow-hidden`}
        >
             <input type="file" accept="image/*" className="hidden" ref={fileInputRef} onChange={handleFileSelect} />
             
             {/* Hover Glow */}
             <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-primary/20 blur-[80px] rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none" />
             
             {preview ? (
                <div className="absolute inset-0 w-full h-full p-4">
                   <img src={preview} alt="Crop Preview" className="w-full h-full object-cover rounded-[2.5rem] shadow-2xl opacity-50 mix-blend-luminosity" />
                </div>
             ) : null}

             {isLoading ? (
                 <div className="relative z-10 flex flex-col items-center text-primary">
                    <Loader2 className="w-12 h-12 mb-4 animate-spin" />
                    <p className="font-outfit font-bold tracking-widest uppercase">Analyzing Tissue...</p>
                 </div>
             ) : (
                <div className="relative z-10 flex flex-col items-center">
                    <div className="w-20 h-20 rounded-full bg-primary flex items-center justify-center mb-6 shadow-ambient-glow group-hover:scale-110 transition-transform duration-500">
                      <Camera className="w-8 h-8 text-surface-container-lowest" />
                    </div>
                    <h3 className="font-outfit text-2xl font-bold mb-2 text-on_surface">{preview ? 'Change Photo' : 'Capture or Upload'}</h3>
                    {error ? (
                        <p className="text-sm text-red-400 font-medium max-w-xs text-center">{error}</p>
                    ) : (
                        <p className="text-sm text-gray-400 text-center max-w-xs">Supported formats: JPG, PNG. Ensure the leaf is well-lit and in focus.</p>
                    )}
                </div>
             )}
        </div>

        {/* Diagnosis Results Right Panel */}
        <div className="md:col-span-2 bg-surface-container-low border border-surface-container-high rounded-[3rem] p-8 relative flex flex-col items-center min-h-[400px]">
            {isLoading ? (
                <div className="absolute inset-0 bg-glass-shimmer opacity-20 animate-pulse rounded-[3rem]" />
            ) : null}

            {!result && !isLoading ? (
                <div className="flex-1 flex flex-col items-center justify-center text-center opacity-40">
                   <Leaf className="w-16 h-16 text-surface-variant mb-4" />
                   <p className="font-outfit font-bold text-xl">Awaiting Scan</p>
                </div>
            ) : null}

            {result ? (
               <>
                {/* Circular Confidence Meter */}
                <div className="relative w-40 h-40 mb-6">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-surface-container" />
                    <circle cx="80" cy="80" r="70" stroke="url(#gradient)" strokeWidth="8" fill="transparent" strokeDasharray="440" strokeDashoffset={440 - (440 * result.confidence) / 100} className="drop-shadow-[0_0_8px_rgba(121,219,141,0.5)] transition-all duration-1000 ease-out" />
                    <defs>
                      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#FFB95F" />
                        <stop offset="100%" stopColor="#79DB8D" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-3xl font-black text-on_surface">{result.confidence}%</span>
                      <span className="text-[10px] font-bold tracking-widest text-gray-500 uppercase mt-1">Confidence</span>
                  </div>
                </div>

                <h2 className="font-outfit text-2xl font-bold text-on_surface mb-1">{result.disease}</h2>
                <p className="text-primary text-sm italic mb-6">{result.scientific_name || "Biological Scan Complete"}</p>

                {/* Pills */}
                <div className="flex gap-2 mb-8 flex-wrap justify-center">
                    {result.symptoms.map(symptom => (
                       <span key={symptom} className="px-3 py-1.5 bg-surface-variant/30 rounded-full text-[10px] font-bold tracking-wider text-gray-300">
                          {symptom}
                       </span>
                    ))}
                </div>

                {/* Accordions */}
                <div className="w-full space-y-3">
                  <div className="w-full bg-surface-container rounded-2xl p-4 flex flex-col gap-2 border border-surface-container-high">
                      <div className="flex items-center gap-3">
                        <FlaskConical className="w-5 h-5 text-secondary" />
                        <span className="text-sm font-bold">Chemical Treatment</span>
                      </div>
                      <div className="text-xs text-gray-400 pl-8 space-y-1">
                          {result.chemical_treatments.map((t, i) => <p key={i}>• {t}</p>)}
                      </div>
                  </div>

                  <div className="w-full bg-surface-container rounded-2xl p-4 flex flex-col gap-2 border border-surface-container-high">
                      <div className="flex items-center gap-3">
                        <Leaf className="w-5 h-5 text-primary" />
                        <span className="text-sm font-bold">Organic Solutions</span>
                      </div>
                      <div className="text-xs text-gray-400 pl-8 space-y-1">
                          {result.organic_treatments.map((t, i) => <p key={i}>• {t}</p>)}
                      </div>
                  </div>
                </div>
               </>
            ) : null}

        </div>

      </div>

      {/* Community Insights Grid */}
      <h3 className="font-outfit text-2xl font-bold mb-6 text-on_surface">Community Insights</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-surface-container-low border border-surface-container-high rounded-[2rem] overflow-hidden flex flex-col group cursor-pointer relative h-[250px]">
             <div className="absolute inset-0 bg-gradient-to-t from-surface-container-lowest via-surface-container-lowest/90 to-transparent z-10" />
             <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1596704017254-9b121068fb31?q=80&w=600&auto=format&fit=crop')] bg-cover bg-center opacity-40 group-hover:opacity-60 transition-opacity duration-500 mix-blend-luminosity" />
             <div className="relative z-20 p-6 mt-auto">
                <div className="w-8 h-8 rounded-full bg-primary/20 backdrop-blur-md flex items-center justify-center mb-4">
                   <ShieldCheck className="w-4 h-4 text-primary" />
                </div>
                <h4 className="font-outfit font-bold text-lg mb-2">Prevention is the best cure</h4>
                <p className="text-xs text-gray-400">Learn how crop rotation and soil management can reduce Early Blight by up to 60%.</p>
             </div>
          </div>
          <div className="bg-surface-container-low border border-surface-container-high rounded-[2rem] overflow-hidden flex flex-col group cursor-pointer relative h-[250px]">
             <div className="absolute inset-0 bg-gradient-to-t from-surface-container-lowest via-surface-container-lowest/90 to-transparent z-10" />
             <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?q=80&w=600&auto=format&fit=crop')] bg-cover bg-center opacity-40 group-hover:opacity-60 transition-opacity duration-500 mix-blend-luminosity" />
             <div className="relative z-20 p-6 mt-auto">
                <div className="w-8 h-8 rounded-full bg-secondary/20 backdrop-blur-md flex items-center justify-center mb-4">
                   <AlertTriangle className="w-4 h-4 text-secondary" />
                </div>
                <h4 className="font-outfit font-bold text-lg mb-2">Regional Alerts</h4>
                <p className="text-xs text-gray-400">High humidity levels detected in your region. Increase monitoring for fungal infections.</p>
             </div>
          </div>
          <div className="bg-surface-container-low border border-surface-container-high rounded-[2rem] overflow-hidden flex flex-col group cursor-pointer relative h-[250px]">
             <div className="absolute inset-0 bg-gradient-to-t from-surface-container-lowest via-surface-container-lowest/90 to-transparent z-10" />
             <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=600&auto=format&fit=crop')] bg-cover bg-center opacity-40 group-hover:opacity-60 transition-opacity duration-500 mix-blend-luminosity" />
             <div className="relative z-20 p-6 mt-auto">
                <div className="w-8 h-8 rounded-full bg-primary/20 backdrop-blur-md flex items-center justify-center mb-4">
                   <Leaf className="w-4 h-4 text-primary" />
                </div>
                <h4 className="font-outfit font-bold text-lg mb-2">Soil Nutrition Guide</h4>
                <p className="text-xs text-gray-400">Ensure proper Nitrogen balance to strengthen cellular walls against pathogens.</p>
             </div>
          </div>
      </div>

    </div>
  )
}
