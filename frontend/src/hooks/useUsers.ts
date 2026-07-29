import { useQuery } from "@tanstack/react-query";
import { usersApi } from "@/api/users";

export const useUsers = () => {
  return useQuery({
    queryKey: ["users"],
    queryFn: usersApi.getAll,
  });
};

export const useUser = (id: string) => {
  return useQuery({
    queryKey: ["users", id],
    queryFn: () => usersApi.getById(id),
    enabled: !!id,
  });
};

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ["users", "me"],
    queryFn: usersApi.me,
  });
};
