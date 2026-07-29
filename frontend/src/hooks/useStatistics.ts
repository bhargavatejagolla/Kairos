import { useQuery } from "@tanstack/react-query";
import { statisticsApi } from "@/api/statistics";

export const usePlatformStatistics = (orgId?: string) => {
  return useQuery({
    queryKey: ["statistics", orgId],
    queryFn: () => statisticsApi.getOverview(orgId),
    refetchInterval: 10000, // Poll every 10 seconds for real-time dashboard updates
  });
};
