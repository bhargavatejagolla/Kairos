import { apiClient } from "./client";

export interface TimelineEvent {
  id: string;
  incident_id: string;
  event_type: string;
  content: string;
  actor_id?: string;
  created_at: string;
}

export interface TimelineEventCreate {
  incident_id: string;
  event_type: string;
  content: string;
  actor_id?: string;
}

export const timelinesApi = {
  getByIncident: async (incidentId: string): Promise<TimelineEvent[]> => {
    const { data } = await apiClient.get<TimelineEvent[]>(`/timelines?incident_id=${incidentId}`);
    return data;
  },
  
  create: async (payload: TimelineEventCreate): Promise<TimelineEvent> => {
    const { data } = await apiClient.post<TimelineEvent>("/timelines", payload);
    return data;
  },
};
