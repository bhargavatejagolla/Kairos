import { apiClient } from "./client";

export interface Incident {
  id: string;
  organization_id: string;
  title: string;
  description?: string;
  status: "investigating" | "identified" | "monitoring" | "resolved";
  severity: "critical" | "high" | "medium" | "low";
  commander_id?: string;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
}

export interface IncidentCreate {
  organization_id: string;
  title: string;
  description?: string;
  status?: "investigating" | "identified" | "monitoring" | "resolved";
  severity?: "critical" | "high" | "medium" | "low";
  commander_id?: string;
}

export const incidentsApi = {
  getAll: async (orgId?: string): Promise<Incident[]> => {
    const url = orgId ? `/incidents?organization_id=${orgId}` : "/incidents";
    const { data } = await apiClient.get<Incident[]>(url);
    return data;
  },
  
  getById: async (id: string): Promise<Incident> => {
    const { data } = await apiClient.get<Incident>(`/incidents/${id}`);
    return data;
  },
  
  create: async (payload: IncidentCreate): Promise<Incident> => {
    const { data } = await apiClient.post<Incident>("/incidents", payload);
    return data;
  },
  
  update: async (id: string, payload: Partial<IncidentCreate>): Promise<Incident> => {
    const { data } = await apiClient.patch<Incident>(`/incidents/${id}`, payload);
    return data;
  },
};
