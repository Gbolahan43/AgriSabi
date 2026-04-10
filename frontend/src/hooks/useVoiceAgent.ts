import { useState, useRef, useEffect, useCallback } from 'react';

/**
 * useVoiceAgent Hook
 * Manages bidirectional WebSocket connection to Amazon Nova Sonic
 * Features: Real-time STT streaming, TTS auto-playback, and persistent state.
 */
export function useVoiceAgent() {
    const [isConnected, setIsConnected] = useState(false);
    const [status, setStatus] = useState<'idle' | 'listening' | 'processing' | 'speaking'>('idle');
    const [currentTranscript, setCurrentTranscript] = useState('');
    const [history, setHistory] = useState<any[]>([]);
    
    const wsRef = useRef<WebSocket | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const sessionIdRef = useRef<string>('');
    const audioContextRef = useRef<AudioContext | null>(null);

    const apiUrl = process.env.NEXT_PUBLIC_API_URL?.replace('https://', 'wss://') || 'wss://akmetmutdx.us-west-2.awsapprunner.com';

    // 1. Connect WebSocket
    const connect = useCallback(async () => {
        if (wsRef.current?.readyState === WebSocket.OPEN) return;

        const sessionId = crypto.randomUUID();
        sessionIdRef.current = sessionId;
        
        // Ensure the path matches the backend route
        const ws = new WebSocket(`${apiUrl}/assistant/stream?session_id=${sessionId}`);
        wsRef.current = ws;

        ws.onopen = () => {
            setIsConnected(true);
            console.log('✅ Voice Assistant Connected');
        };

        ws.onmessage = async (event) => {
            if (typeof event.data === 'string') {
                // Nova Sonic text outputs (subtitles/partial transcripts)
                setCurrentTranscript(prev => prev + ' ' + event.data);
                setStatus('processing');
                
                // Clear transcript and move to history eventually
                // (Logic can be refined based on end-of-turn markers from Nova)
            } else if (event.data instanceof Blob) {
                // Auto-play the Audio Output Chunk (24kHz PCM / MP3)
                setStatus('speaking');
                const audioUrl = URL.createObjectURL(event.data);
                const audio = new Audio(audioUrl);
                audio.onended = () => setStatus('idle');
                audio.play().catch(console.error);
            }
        };

        ws.onclose = () => {
            setIsConnected(false);
            setStatus('idle');
        };
        
        ws.onerror = (err) => console.error('WS Error:', err);

    }, [apiUrl]);

    // 2. Start/Stop Recording
    const startSpeaking = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: { 
                    sampleRate: 16000, 
                    channelCount: 1, 
                    echoCancellation: true,
                    noiseSuppression: true
                } 
            });
            
            setStatus('listening');
            setCurrentTranscript('');

            // We use a shorter timeslice for "live" feel
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
                    wsRef.current.send(e.data);
                }
            };

            mediaRecorder.start(500); // Send audio chunks every 500ms
            
        } catch (err) {
            console.error('Microphone Access Denied:', err);
        }
    };

    const stopSpeaking = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
            mediaRecorderRef.current.stop();
            mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
            setStatus('processing');
        }
    };

    // 3. History Fetching (Optional utility)
    const fetchHistory = async () => {
        const httpUrl = apiUrl.replace('wss://', 'https://');
        try {
            const res = await fetch(`${httpUrl}/api/history/${sessionIdRef.current}`);
            if (res.ok) {
                const data = await res.json();
                setHistory(data.history || []);
            }
        } catch (e) {
            console.error('History fetch failed:', e);
        }
    };

    useEffect(() => {
        connect();
        return () => wsRef.current?.close();
    }, [connect]);

    return { 
        isConnected, 
        status,
        currentTranscript,
        startSpeaking, 
        stopSpeaking,
        history, 
        fetchHistory 
    };
}
