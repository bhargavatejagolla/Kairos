import { apiClient } from "./client";

export interface Project {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  organization_id: string;
  name: string;
  description?: string;
}

export const projectsApi = {
  getAll: async (orgId?: string): Promise<Project[]> => {
    const url = orgId ? `/projects?organization_id=${orgId}` : "/projects";
    const { data } = await apiClient.get<Project[]>(url);
    return data;
  },
  
  getById: async (id: string): Promise<Project> => {
    const { data } = await apiClient.get<Project>(`/projects/${id}`);
    return data;
  },
  
  create: async (payload: ProjectCreate): Promise<Project> => {
    const { data } = await apiClient.post<Project>("/projects", payload);
    return data;
  },
  
  update: async (id: string, payload: Partial<ProjectCreate>): Promise<Project> => {
    const { data } = await apiClient.patch<Project>(`/projects/${id}`, payload);
    return data;
  },
  
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/projects/${id}`);
  },
};
