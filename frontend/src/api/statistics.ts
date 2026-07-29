import { apiClient } from "./client";

export interface PlatformStatistics {
  total_incidents: number;
  active_incidents: number;
  total_alerts: number;
  active_alerts: number;
  mttr: number; // Mean Time to Resolve in minutes
  mtta: number; // Mean Time to Acknowledge in minutes
}

export const statisticsApi = {
  getOverview: async (orgId?: string): Promise<PlatformStatistics> => {
    const url = orgId ? `/statistics/overview?organization_id=${orgId}` : "/statistics/overview";
    const { data } = await apiClient.get<PlatformStatistics>(url);
    return data;
  },
};
