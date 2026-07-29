import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { organizationsApi, type OrganizationCreate } from "@/api/organizations";

export const useOrganizations = () => {
  return useQuery({
    queryKey: ["organizations"],
    queryFn: organizationsApi.getAll,
  });
};

export const useOrganization = (id: string) => {
  return useQuery({
    queryKey: ["organizations", id],
    queryFn: () => organizationsApi.getById(id),
    enabled: !!id,
  });
};

export const useCreateOrganization = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: OrganizationCreate) => organizationsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
    },
  });
};
