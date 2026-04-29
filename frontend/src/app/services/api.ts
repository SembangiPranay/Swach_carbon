/**
 * API Service - Bridges frontend form model to backend API
 */

import { FormData, EmissionResults } from '../components/Root';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface CalculationResponse {
  calculation_id: string;
}

export interface StreamEvent {
  type: 'thought' | 'action' | 'observation' | 'complete' | 'error';
  content: string;
  timestamp?: string;
}

/**
 * Map frontend form data to backend request format
 */
function mapFormDataToBackend(formData: FormData) {
  // Backend expects these specific fields in ActivityDataRequest
  // Map all frontend fields to backend field names exactly
  return {
    company_name: formData.companyName,
    industry: formData.industry,
    employee_count: formData.employeeCount || 1,
    
    electricity_kwh: formData.electricity,
    diesel_litres: formData.diesel,
    petrol_litres: formData.petrol,
    natural_gas_m3: formData.naturalGas,
    lpg_kg: formData.lpg,
    coal_tonnes: formData.coal,
    
    waste_kg: formData.waste,
    water_m3: formData.water,
    
    // Business travel is split: air (flights) vs road (commute)
    flights_km: formData.businessTravel * 0.7, // Assume 70% air travel
    commute_km: formData.businessTravel * 0.3, // Assume 30% road travel
  };
}

/**
 * Start a calculation on the backend
 */
export async function startCalculation(formData: FormData): Promise<CalculationResponse> {
  const payload = mapFormDataToBackend(formData);

  const response = await fetch(`${API_BASE_URL}/calculate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Upload an image to analyze a utility bill
 */
export async function analyzeBill(file: File, billType: string = 'electricity'): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/analyze-bill?bill_type=${billType}`, {
    method: 'POST',
    body: formData, // fetch will set multipart/form-data boundary automatically
  });

  if (!response.ok) {
    throw new Error(`Analysis error: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Stream calculation events from the backend
 * Returns an async generator that yields events
 */
export async function* streamCalculationEvents(
  calculationId: string
): AsyncGenerator<StreamEvent> {
  const response = await fetch(`${API_BASE_URL}/stream?id=${calculationId}`);

  if (!response.ok) {
    throw new Error(`Stream error: ${response.statusText}`);
  }

  if (!response.body) {
    throw new Error('No response body');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');

      // Process complete lines
      for (let i = 0; i < lines.length - 1; i++) {
        const line = lines[i].trim();

        if (line.startsWith('data: ')) {
          const jsonStr = line.slice(6);
          try {
            const event = JSON.parse(jsonStr) as StreamEvent;
            yield event;
          } catch (e) {
            console.error('Failed to parse event:', jsonStr);
          }
        }
      }

      // Keep incomplete line in buffer
      buffer = lines[lines.length - 1];
    }

    // Process remaining buffer
    if (buffer.trim().startsWith('data: ')) {
      const jsonStr = buffer.slice(6).trim();
      try {
        const event = JSON.parse(jsonStr) as StreamEvent;
        yield event;
      } catch (e) {
        console.error('Failed to parse final event:', jsonStr);
      }
    }
  } finally {
    reader.releaseLock();
  }
}

/**
 * Get the PDF report
 */
export async function downloadReport(calculationId: string): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}/report?id=${calculationId}`);

  if (!response.ok) {
    throw new Error(`Report error: ${response.statusText}`);
  }

  return response.blob();
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }

  return response.json();
}
