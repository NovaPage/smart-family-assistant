export interface ChatMessage {
  sender: 'user' | 'assistant';
  content: string;
}

export interface AssistantRequest {
  message: string;
  source: 'web';
}

export interface AssistantResponse {
  response: string;
  reply: string;
}
