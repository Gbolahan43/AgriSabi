"use client"
import React, { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import { Send, ImagePlus, Mic, Stethoscope, Loader2, ArrowLeft, Bot, User, Leaf, StopCircle, X } from 'lucide-react'
import * as api from '@/lib/api'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

type Message = {
  id: string;
  role: 'user' | 'assistant';
  type: 'text' | 'diagnosis' | 'image_preview';
  content?: string;
  imageUrl?: string;
  diagnosisData?: api.DiagnosisResponse;
};

export default function OmniChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      type: 'text',
      content: "Welcome to AgriSabi! Ask me anything about your farm, check today's weather, or upload a photo to immediately diagnose a sick crop."
    }
  ]);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [sessionId, setSessionId] = useState<string>("");
  const [stagedImage, setStagedImage] = useState<File | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    let currentSession = localStorage.getItem("agrisabi_session_id");
    if (!currentSession) {
      currentSession = `session_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem("agrisabi_session_id", currentSession);
    }
    setSessionId(currentSession);

    api.getChatHistory(currentSession).then(history => {
      if (history && history.length > 0) {
        const mappedHistory: Message[] = history.map((item: any, index: number) => ({
          id: `hist_${index}`,
          role: item.role,
          type: 'text',
          content: item.content[0].text
        }));
        setMessages([
          { id: 'welcome', role: 'assistant', type: 'text', content: "Welcome back! Continuing your conversation." },
          ...mappedHistory
        ]);
      }
    }).catch(err => console.log("No history found or error", err));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping, stagedImage]);

  const handleTextSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputText.trim() && !stagedImage) return;

    const userText = inputText;
    const currentImage = stagedImage;
    
    setInputText("");
    setStagedImage(null);
    
    const userMsgId = Date.now().toString();
    if (currentImage) {
        const previewUrl = URL.createObjectURL(currentImage);
        setMessages(prev => [...prev, { 
          id: userMsgId, 
          role: 'user', 
          type: 'image_preview', 
          imageUrl: previewUrl,
          content: userText 
        }]);
    } else {
        setMessages(prev => [...prev, { id: userMsgId, role: 'user', type: 'text', content: userText }]);
    }
    
    setIsTyping(true);
    try {
      if (currentImage) {
         const result = await api.uploadForDiagnosis(currentImage, userText, sessionId);
         setMessages(prev => [...prev, {
            id: Date.now().toString(),
            role: 'assistant',
            type: 'diagnosis',
            diagnosisData: result
         }]);
      } else {
         const response = await api.sendChatMessage(userText, sessionId);
         setMessages(prev => [...prev, { 
            id: Date.now().toString(), 
            role: 'assistant', 
            type: 'text', 
            content: response.message 
         }]);
      }
    } catch (error: any) {
      setMessages(prev => [...prev, { 
        id: Date.now().toString(), 
        role: 'assistant', 
        type: 'text', 
        content: error.message || "Network error: Failed to reach AgriSabi core." 
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const toggleRecording = async () => {
    if (isRecording) {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        stream.getTracks().forEach(track => track.stop());
        
        setIsTyping(true);
        try {
          const transcribedText = await api.transcribeAudio(audioBlob);
          if (transcribedText) setInputText(transcribedText);
        } catch (err) {
          console.error("STT Error:", err);
          alert("Failed to transcribe audio.");
        } finally {
          setIsTyping(false);
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Mic error:", err);
      alert("Microphone access denied or unavailable.");
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setStagedImage(file);
    e.target.value = '';
  };

  return (
    <div className="min-h-screen bg-surface flex flex-col md:flex-row">
      
      {/* Omni-Chat Sidebar */}
      <aside className="w-full md:w-64 bg-surface-container-low border-b md:border-b-0 md:border-r border-surface-container-high p-4 flex flex-col gap-4">
        <Link href="/" className="inline-flex items-center gap-2 text-primary font-semibold hover:opacity-80 transition-opacity pb-4 border-b border-surface-container-high">
          <ArrowLeft className="w-4 h-4" /> Back Home
        </Link>
        <div className="flex-1">
          <h2 className="text-xs font-bold text-surface-container-highest tracking-wider uppercase mb-3">Quick Tools</h2>
          <Link href="/diagnose" className="w-full flex items-center gap-3 p-3 rounded-xl bg-surface-container hover:bg-surface-container-high transition-colors mb-2 text-sm text-on_surface font-medium border border-transparent hover:border-primary/20">
            <Stethoscope className="w-4 h-4 text-primary" /> Deep Diagnosis Hub
          </Link>
          <Link href="/assistant" className="w-full flex items-center gap-3 p-3 rounded-xl bg-surface-container hover:bg-surface-container-high transition-colors text-sm text-on_surface font-medium border border-transparent hover:border-secondary/20">
            <Mic className="w-4 h-4 text-secondary" /> Live Voice Assistant
          </Link>
        </div>
        <div className="mt-auto hidden md:block pt-4 border-t border-surface-container-high">
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <Leaf className="w-3 h-3 text-primary" /> Powered by AWS Bedrock
          </div>
        </div>
      </aside>

      {/* Main Chat Interface */}
      <main className="flex-1 flex flex-col relative h-[calc(100vh-64px)] md:h-screen">
        
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
          {messages.map(msg => (
            <div key={msg.id} className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] md:max-w-[70%] flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1 ${msg.role === 'user' ? 'bg-surface-container-high' : 'bg-primary/20 text-primary'}`}>
                  {msg.role === 'user' ? <User className="w-4 h-4 text-gray-400" /> : <Bot className="w-4 h-4" />}
                </div>
                
                {msg.type === 'text' && (
                  <div className={`p-4 rounded-2xl ${msg.role === 'user' ? 'bg-surface-container border border-surface-container-high text-on_surface' : 'bg-primary/10 border border-primary/20 text-on_surface lg:px-6'}`}>
                    <div className="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-headings:text-primary prose-a:text-secondary hover:prose-a:underline">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content || ""}</ReactMarkdown>
                    </div>
                  </div>
                )}
                
                {msg.type === 'image_preview' && (
                  <div className="p-2 rounded-2xl bg-surface-container border border-surface-container-high flex flex-col gap-2">
                    <img src={msg.imageUrl} alt="Uploaded for diagnosis" className="max-w-[200px] md:max-w-[300px] rounded-xl object-cover" />
                    {msg.content && (
                      <div className="px-2 pb-2">
                         <p className="text-sm text-on_surface">{msg.content}</p>
                      </div>
                    )}
                  </div>
                )}
                
                {msg.type === 'diagnosis' && msg.diagnosisData && (
                  <div className="p-5 rounded-2xl bg-surface-container-low border border-primary/30 shadow-ambient-glow w-full lg:min-w-[400px]">
                    <div className="flex items-center gap-3 mb-4">
                      <Stethoscope className="w-5 h-5 text-primary" />
                      <h3 className="font-outfit font-bold text-lg text-primary">Diagnostic Report</h3>
                    </div>
                    
                    <div className="mb-4">
                      <span className="text-sm text-gray-400 font-medium tracking-wide uppercase">Identified Condition</span>
                      <p className="text-xl font-bold text-on_surface">{msg.diagnosisData.disease}</p>
                      {msg.diagnosisData.scientific_name && (
                        <p className="text-sm italic text-gray-500">{msg.diagnosisData.scientific_name}</p>
                      )}
                    </div>
                    
                    <div className="flex items-center gap-3 mb-6 bg-surface-container p-3 rounded-xl border border-surface-container-high">
                      <div className="relative w-12 h-12 flex items-center justify-center">
                        <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                          <path className="text-surface-container-high" strokeWidth="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                          <path className="text-primary" strokeDasharray={`${msg.diagnosisData.confidence}, 100`} strokeWidth="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        </svg>
                        <span className="absolute text-xs font-bold text-on_surface">{msg.diagnosisData.confidence}%</span>
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-on_surface">AI Confidence Level</p>
                        <p className="text-xs text-gray-400">Based on purely visual symptoms matching RAG data.</p>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      {msg.diagnosisData.organic_treatments && msg.diagnosisData.organic_treatments.length > 0 && (
                        <div>
                          <p className="text-sm font-bold text-secondary mb-2 flex items-center gap-2"><Leaf className="w-4 h-4"/> Organic Treatment</p>
                          <ul className="list-disc pl-5 text-sm text-gray-300 space-y-1">
                            {msg.diagnosisData.organic_treatments.map((t, i) => <li key={i}>{t}</li>)}
                          </ul>
                        </div>
                      )}
                      {msg.diagnosisData.chemical_treatments && msg.diagnosisData.chemical_treatments.length > 0 && (
                        <div className="pt-3 border-t border-surface-container-high">
                          <p className="text-sm font-bold text-amber-500 mb-2">Chemical Treatment</p>
                          <ul className="list-disc pl-5 text-sm text-gray-300 space-y-1">
                            {msg.diagnosisData.chemical_treatments.map((t, i) => <li key={i}>{t}</li>)}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                )}
                
              </div>
            </div>
          ))}
          
          {isTyping && (
             <div className="flex w-full justify-start">
               <div className="flex gap-3 flex-row">
                 <div className="w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center flex-shrink-0 mt-1">
                   <Loader2 className="w-4 h-4 animate-spin" />
                 </div>
                 <div className="p-4 rounded-2xl bg-primary/5 border border-primary/10">
                   <span className="text-sm text-gray-400 animate-pulse">AgriSabi is thinking...</span>
                 </div>
               </div>
             </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-surface border-t border-surface-container-high">
          
          {/* Staged Image Preview Area */}
          {stagedImage && (
            <div className="max-w-4xl mx-auto mb-3 relative inline-block">
               <div className="relative inline-block border-2 border-primary/50 rounded-xl p-1 bg-surface-container">
                 <img src={URL.createObjectURL(stagedImage)} className="h-20 max-w-[120px] object-cover rounded-lg" />
                 <button 
                   type="button"
                   onClick={() => setStagedImage(null)} 
                   className="absolute -top-2 -right-2 bg-surface-container-highest text-white rounded-full p-1 hover:bg-red-500 transition-colors shadow-lg"
                 >
                   <X className="w-4 h-4" />
                 </button>
               </div>
            </div>
          )}

          <form onSubmit={handleTextSubmit} className="max-w-4xl mx-auto relative flex items-center gap-2">
            <input type="file" accept="image/*" capture="environment" className="hidden" ref={fileInputRef} onChange={handleImageUpload} />
            <button type="button" onClick={() => fileInputRef.current?.click()} className="p-3 rounded-full bg-surface-container-low text-primary hover:bg-surface-container hover:text-primary-light transition-colors flex-shrink-0 tooltip-trigger">
              <ImagePlus className="w-5 h-5" />
            </button>
            <button type="button" onClick={toggleRecording} className={`p-3 rounded-full transition-colors flex-shrink-0 tooltip-trigger ${isRecording ? 'bg-red-500/20 text-red-500 animate-pulse' : 'bg-surface-container-low text-secondary hover:bg-surface-container hover:text-secondary-light'}`}>
              {isRecording ? <StopCircle className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>
            
            <div className="flex-1 relative flex items-center">
              <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} placeholder={isRecording ? "Listening..." : "Ask about weather, soil, or paste image..."} disabled={isRecording} className="w-full bg-surface-container-lowest border border-surface-container-high text-on_surface rounded-full py-4 pl-6 pr-14 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all font-inter disabled:opacity-50" />
              <button type="submit" disabled={(!inputText.trim() && !stagedImage) || isTyping || isRecording} className="absolute right-2 p-2 rounded-full bg-primary text-surface hover:scale-105 disabled:opacity-50 disabled:hover:scale-100 transition-all">
                <Send className="w-4 h-4" />
              </button>
            </div>
          </form>
        </div>
        
      </main>
    </div>
  )
}
