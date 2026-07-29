import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { incidentsApi, type IncidentCreate } from "@/api/incidents";

export const useIncidents = (orgId?: string) => {
  return useQuery({
    queryKey: ["incidents", orgId],
    queryFn: () => incidentsApi.getAll(orgId),
  });
};

export const useIncident = (id: string) => {
  return useQuery({
    queryKey: ["incidents", id],
    queryFn: () => incidentsApi.getById(id),
    enabled: !!id,
  });
};

export const useCreateIncident = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: IncidentCreate) => incidentsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["incidents"] });
    },
  });
};
