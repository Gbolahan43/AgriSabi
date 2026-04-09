const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface DiagnosisResponse {
  disease: string;
  confidence: number;
  scientific_name?: string;
  symptoms: string[];
  organic_treatments: string[];
  chemical_treatments: string[];
}

export async function uploadForDiagnosis(file: File): Promise<DiagnosisResponse> {
  const formData = new FormData();
  formData.append("file", file);

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
