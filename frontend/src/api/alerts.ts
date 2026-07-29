import { apiClient } from "./client";

export interface Alert {
  id: string;
  organization_id: string;
  project_id?: string;
  service_id?: string;
  incident_id?: string;
  title: string;
  description?: string;
  status: "firing" | "acknowledged" | "resolved";
  severity: "critical" | "warning" | "info";
  source: string;
  created_at: string;
}

export const alertsApi = {
  getAll: async (orgId?: string): Promise<Alert[]> => {
    const url = orgId ? `/alerts?organization_id=${orgId}` : "/alerts";
    const { data } = await apiClient.get<Alert[]>(url);
    return data;
  },
  
  getById: async (id: string): Promise<Alert> => {
    const { data } = await apiClient.get<Alert>(`/alerts/${id}`);
    return data;
  },
  
  acknowledge: async (id: string): Promise<Alert> => {
    const { data } = await apiClient.post<Alert>(`/alerts/${id}/acknowledge`);
    return data;
  },
};
