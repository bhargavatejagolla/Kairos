import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { alertsApi } from "@/api/alerts";

export const useAlerts = (orgId?: string) => {
  return useQuery({
    queryKey: ["alerts", orgId],
    queryFn: () => alertsApi.getAll(orgId),
  });
};

export const useAlert = (id: string) => {
  return useQuery({
    queryKey: ["alerts", id],
    queryFn: () => alertsApi.getById(id),
    enabled: !!id,
  });
};

export const useAcknowledgeAlert = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => alertsApi.acknowledge(id),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["alerts"] });
      queryClient.invalidateQueries({ queryKey: ["alerts", variables] });
    },
  });
};
