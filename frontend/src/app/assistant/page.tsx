"use client"
import { useVoiceAgent } from '@/hooks/useVoiceAgent';
import { Mic, Square, Volume2, History, Info, ChevronRight, Speaker } from 'lucide-react';
import Link from 'next/link';

export default function AssistantPage() {
    const { 
        isConnected, 
        status, 
        currentTranscript, 
        startSpeaking, 
        stopSpeaking, 
        history, 
        fetchHistory 
    } = useVoiceAgent();

    return (
        <div className="min-h-screen bg-surface flex flex-col items-center justify-center px-4 md:px-8 relative overflow-hidden">
            {/* Ambient Background Glows */}
            <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full blur-[120px] transition-all duration-1000 -z-10 ${
                status === 'listening' ? 'bg-primary/30' : 
                status === 'speaking' ? 'bg-secondary/30' : 'bg-surface-container/20'
            }`} />

            <div className="w-full max-w-2xl flex flex-col items-center">
                {/* Status Badge */}
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-surface-container-low border border-surface-container-high/50 mb-12 backdrop-blur-md">
                    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-primary animate-pulse' : 'bg-red-500'}`} />
                    <span className="text-[10px] font-bold tracking-widest uppercase text-gray-400">
                        {isConnected ? 'Nova Sonic Live' : 'Connecting to Core...'}
                    </span>
                </div>

                <h1 className="font-outfit text-4xl md:text-5xl font-black text-on_surface mb-4 text-center">
                    AgriSabi <span className="text-primary">Voice</span>
                </h1>
                <p className="text-gray-400 text-center mb-16 max-w-md">
                    Ask questions about your crops in plain English. Your advisor is listening and ready to speak.
                </p>

                {/* Main Interactive Sphere/Button */}
                <div className="relative mb-20 group">
                    {/* Visualizer Rings */}
                    <div className={`absolute inset-0 rounded-full border border-primary/20 transition-all duration-500 ${status === 'listening' ? 'scale-150 opacity-0 animate-ping' : 'scale-100 opacity-0'}`} />
                    <div className={`absolute inset-0 rounded-full border-2 border-primary/10 transition-all duration-700 delay-150 ${status === 'listening' ? 'scale-125 opacity-0 animate-ping' : 'scale-100 opacity-0'}`} />

                    <button 
                        onMouseDown={startSpeaking}
                        onMouseUp={stopSpeaking}
                        onTouchStart={startSpeaking}
                        onTouchEnd={stopSpeaking}
                        disabled={!isConnected}
                        className={`relative w-32 h-32 md:w-40 md:h-40 rounded-full flex flex-col items-center justify-center transition-all duration-300 shadow-ambient-glow border-4 ${
                            status === 'listening' 
                            ? 'bg-primary border-white/20 scale-105' 
                            : 'bg-surface-container-low border-surface-container-high hover:border-primary/50'
                        }`}
                    >
                        {status === 'listening' ? (
                            <Square className="w-10 h-10 text-surface fill-current" />
                        ) : (
                            <Mic className={`w-12 h-12 ${isConnected ? 'text-primary' : 'text-gray-600'}`} />
                        )}
                        <span className={`absolute -bottom-10 text-[10px] font-bold tracking-widest uppercase transition-colors ${status === 'listening' ? 'text-primary' : 'text-gray-500'}`}>
                            {status === 'listening' ? 'Release to Send' : 'Hold to Speak'}
                        </span>
                    </button>
                </div>

                {/* Live Transcript / Feedback UI */}
                <div className="w-full bg-surface-container-low/50 backdrop-blur-xl border border-surface-container-high rounded-[2.5rem] p-8 mb-8 text-center min-h-[140px] flex flex-col items-center justify-center relative shadow-2xl">
                    <div className="absolute top-4 left-6 flex items-center gap-2 text-gray-500">
                        <Volume2 className="w-4 h-4" />
                        <span className="text-[10px] font-bold tracking-tighter uppercase uppercase">Real-time Feedback</span>
                    </div>

                    {status === 'idle' && !currentTranscript && (
                        <div className="space-y-2 opacity-40">
                            <p className="text-sm italic">"How can I help you today?"</p>
                            <p className="text-[10px] uppercase font-bold tracking-widest">Try: What are the symptoms of early rust?</p>
                        </div>
                    )}
                    
                    {status === 'listening' && (
                        <div className="flex flex-col items-center gap-4">
                            <div className="flex gap-1">
                                {[1,2,3,4,5].map(i => (
                                    <div key={i} className={`w-1 bg-primary rounded-full animate-pulse`} style={{ height: `${Math.random() * 24 + 8}px`, animationDelay: `${i * 0.1}s` }} />
                                ))}
                            </div>
                            <p className="text-primary font-medium">Listening...</p>
                        </div>
                    )}

                    {(status === 'processing' || status === 'speaking' || currentTranscript) && (
                        <p className="text-on_surface leading-relaxed max-w-lg">
                            {currentTranscript || "Processing your request..."}
                        </p>
                    )}
                </div>

                {/* Quick Actions / Bottom Tools */}
                <div className="flex gap-4 w-full">
                    <button 
                        onClick={fetchHistory}
                        className="flex-1 bg-surface-container p-4 rounded-2xl border border-surface-container-high flex items-center justify-between hover:border-primary/30 transition-all group"
                    >
                        <div className="flex items-center gap-3">
                            <History className="w-5 h-5 text-gray-400 group-hover:text-primary transition-colors" />
                            <span className="text-sm font-semibold text-gray-300">View History</span>
                        </div>
                        <ChevronRight className="w-4 h-4 text-gray-600" />
                    </button>

                    <Link 
                        href="/chat"
                        className="flex-1 bg-surface-container p-4 rounded-2xl border border-surface-container-high flex items-center justify-between hover:border-primary/30 transition-all group"
                    >
                        <div className="flex items-center gap-3">
                            <Speaker className="w-5 h-5 text-gray-400 group-hover:text-primary transition-colors" />
                            <span className="text-sm font-semibold text-gray-300">Switch to Text</span>
                        </div>
                        <ChevronRight className="w-4 h-4 text-gray-600" />
                    </Link>
                </div>
            </div>
        </div>
    );
}
