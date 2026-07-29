import { apiClient } from "./client";

export interface AuditLog {
  id: string;
  organization_id: string;
  actor_id?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  details?: Record<string, any>;
  ip_address?: string;
  created_at: string;
}

export const auditApi = {
  getAll: async (orgId?: string): Promise<AuditLog[]> => {
    const url = orgId ? `/audit/logs?organization_id=${orgId}` : "/audit/logs";
    const { data } = await apiClient.get<AuditLog[]>(url);
    return data;
  },
};
