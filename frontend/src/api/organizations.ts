import { apiClient } from "./client";

export interface Organization {
  id: string;
  name: string;
  slug: string;
  domain?: string;
  tier: string;
  created_at: string;
  updated_at: string;
}

export interface OrganizationCreate {
  name: string;
  slug?: string;
  domain?: string;
  tier?: string;
}

export const organizationsApi = {
  getAll: async (): Promise<Organization[]> => {
    const { data } = await apiClient.get<Organization[]>("/organizations");
    return data;
  },
  
  getById: async (id: string): Promise<Organization> => {
    const { data } = await apiClient.get<Organization>(`/organizations/${id}`);
    return data;
  },
  
  create: async (payload: OrganizationCreate): Promise<Organization> => {
    const { data } = await apiClient.post<Organization>("/organizations", payload);
    return data;
  },
  
  update: async (id: string, payload: Partial<OrganizationCreate>): Promise<Organization> => {
    const { data } = await apiClient.patch<Organization>(`/organizations/${id}`, payload);
    return data;
  },
  
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/organizations/${id}`);
  },
};
