import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { timelinesApi, type TimelineEventCreate } from "@/api/timelines";

export const useIncidentTimeline = (incidentId: string) => {
  return useQuery({
    queryKey: ["timelines", incidentId],
    queryFn: () => timelinesApi.getByIncident(incidentId),
    enabled: !!incidentId,
    refetchInterval: 5000, // Poll every 5 seconds for real-time feel
  });
};

export const useCreateTimelineEvent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: TimelineEventCreate) => timelinesApi.create(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["timelines", variables.incident_id] });
    },
  });
};
