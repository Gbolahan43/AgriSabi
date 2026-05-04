const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface DiagnosisResponse {
  disease: string;
  confidence: number;
  scientific_name?: string;
  symptoms: string[];
  organic_treatments: string[];
  chemical_treatments: string[];
}

export async function uploadForDiagnosis(file: File, text?: string, sessionId?: string): Promise<DiagnosisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  if (text) formData.append("text", text);
  if (sessionId) formData.append("session_id", sessionId);

  const response = await fetch(`${API_BASE_URL}/diagnose/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to diagnose crop. Please try a clearer image.");
  }

  return response.json();
}

export interface ChatResponse {
  response: string; // Backend ChatResponse schema field
}

export async function sendChatMessage(message: string, sessionId: string = "default_session"): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to send message.");
  }

  const data: ChatResponse = await response.json();
  // Normalize backend 'response' field → frontend 'message' field
  return { message: data.response };
}

export async function getChatHistory(sessionId: string): Promise<any[]> {
  const response = await fetch(`${API_BASE_URL}/api/${sessionId}`);
  if (!response.ok) {
    // If not found, just return empty
    if (response.status === 404) return [];
    throw new Error("Failed to load history.");
  }
  const data = await response.json();
  return data.history || [];
}

export async function transcribeAudio(audioBlob: Blob): Promise<string> {
  const formData = new FormData();
  formData.append("file", audioBlob, "voice.webm");

  const response = await fetch(`${API_BASE_URL}/chat/transcribe`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to transcribe audio.");
  }

  const data = await response.json();
  return data.text || "";
}
