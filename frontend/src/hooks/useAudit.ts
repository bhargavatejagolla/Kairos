import { useQuery } from "@tanstack/react-query";
import { auditApi } from "@/api/audit";

export const useAuditLogs = (orgId?: string) => {
  return useQuery({
    queryKey: ["audit", orgId],
    queryFn: () => auditApi.getAll(orgId),
  });
};
