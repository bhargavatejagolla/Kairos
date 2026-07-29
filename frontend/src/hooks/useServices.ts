import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { servicesApi, type ServiceCreate } from "@/api/services";

export const useServices = (projectId?: string) => {
  return useQuery({
    queryKey: ["services", projectId],
    queryFn: () => servicesApi.getAll(projectId),
  });
};

export const useService = (id: string) => {
  return useQuery({
    queryKey: ["services", id],
    queryFn: () => servicesApi.getById(id),
    enabled: !!id,
  });
};

export const useCreateService = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ServiceCreate) => servicesApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["services"] });
    },
  });
};
