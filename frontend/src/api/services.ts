import { apiClient } from "./client";

export interface Service {
  id: string;
  project_id: string;
  name: string;
  description?: string;
  tier: string;
  repository_url?: string;
  created_at: string;
  updated_at: string;
}

export interface ServiceCreate {
  project_id: string;
  name: string;
  description?: string;
  tier?: string;
  repository_url?: string;
}

export const servicesApi = {
  getAll: async (projectId?: string): Promise<Service[]> => {
    const url = projectId ? `/services?project_id=${projectId}` : "/services";
    const { data } = await apiClient.get<Service[]>(url);
    return data;
  },
  
  getById: async (id: string): Promise<Service> => {
    const { data } = await apiClient.get<Service>(`/services/${id}`);
    return data;
  },
  
  create: async (payload: ServiceCreate): Promise<Service> => {
    const { data } = await apiClient.post<Service>("/services", payload);
    return data;
  },
  
  update: async (id: string, payload: Partial<ServiceCreate>): Promise<Service> => {
    const { data } = await apiClient.patch<Service>(`/services/${id}`, payload);
    return data;
  },
  
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/services/${id}`);
  },
};
