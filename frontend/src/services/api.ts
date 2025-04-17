import axios from 'axios';

const API_BASE_URL = 'http://0.0.0.0:8000';

export interface Transcription {
  id: number;
  audio_file_name: string;
  transcribed_text: string;
  created_at: string;
  updated_at: string;
}

interface TranscriptionResponse {
  filename: string;
  status: 'success' | 'error';
  transcription?: Transcription;
  message?: string;
}

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const checkHealth = async (): Promise<boolean> => {
  try {
    const response = await api.get('/health');
    return response.status === 200;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

export const uploadAudioFiles = async (files: File[]): Promise<TranscriptionResponse[]> => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('audio_files', file);
  });

  const response = await api.post<TranscriptionResponse[]>('/transcribe', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getAllTranscriptions = async (): Promise<Transcription[]> => {
  const response = await api.get<Transcription[]>('/transcriptions');
  return response.data;
};

export const searchTranscriptions = async (keyword: string): Promise<Transcription[]> => {
  const response = await api.get<Transcription[]>(`/search?query=${encodeURIComponent(keyword)}`);
  return response.data;
}; 