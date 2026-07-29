import { useParams } from "react-router-dom";
import { useIncident } from "@/hooks/useIncidents";
import { useIncidentTimeline, useCreateTimelineEvent } from "@/hooks/useTimelines";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Activity, Clock, Send, MessageSquare } from "lucide-react";
import { format } from "date-fns";
import { useState } from "react";

export function IncidentDetails() {
  const { id } = useParams<{ id: string }>();
  const { data: incident, isLoading: incidentLoading } = useIncident(id!);
  const { data: timeline, isLoading: timelineLoading } = useIncidentTimeline(id!);
  const createEvent = useCreateTimelineEvent();
  
  const [updateMsg, setUpdateMsg] = useState("");

  if (incidentLoading || timelineLoading) return <div className="p-8">Loading war room...</div>;
  if (!incident) return <div className="p-8 text-destructive">Incident not found</div>;

  const handlePostUpdate = () => {
    if (!updateMsg.trim()) return;
    createEvent.mutate({
      incident_id: incident.id,
      event_type: "update",
      content: updateMsg,
    });
    setUpdateMsg("");
  };

  return (
    <div className="space-y-6 h-[calc(100vh-8rem)] flex flex-col">
      <div className="flex items-center justify-between flex-shrink-0">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold tracking-tight">{incident.title}</h1>
            <Badge variant={incident.severity === "critical" ? "destructive" : "secondary"} className="uppercase">
              {incident.severity}
            </Badge>
            <Badge variant="outline" className="uppercase">
              {incident.status}
            </Badge>
          </div>
          <p className="text-muted-foreground">{incident.description || "No description provided."}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Update Status</Button>
          <Button variant="default">Resolve Incident</Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3 flex-1 min-h-0">
        {/* Timeline Column */}
        <Card className="md:col-span-2 flex flex-col min-h-0 border-border">
          <CardHeader className="flex-shrink-0">
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Incident Timeline
            </CardTitle>
            <CardDescription>Real-time chronological events and communication.</CardDescription>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col min-h-0 p-0">
            <ScrollArea className="flex-1 px-6">
              <div className="space-y-8 py-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
                {timeline?.map((event) => (
                  <div key={event.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div className="flex items-center justify-center w-10 h-10 rounded-full border border-background bg-secondary text-secondary-foreground shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow">
                      {event.event_type === "status_change" ? <Activity size={16} /> : <MessageSquare size={16} />}
                    </div>
                    <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded border border-border bg-card shadow">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold text-sm capitalize">{event.event_type}</span>
                        <time className="text-xs text-muted-foreground">
                          {format(new Date(event.created_at), "HH:mm:ss")}
                        </time>
                      </div>
                      <p className="text-sm text-muted-foreground">{event.content}</p>
                    </div>
                  </div>
                ))}
                {(!timeline || timeline.length === 0) && (
                  <div className="text-center text-muted-foreground text-sm pt-8">No events recorded yet.</div>
                )}
              </div>
            </ScrollArea>
            
            <div className="p-4 border-t border-border mt-auto flex-shrink-0 bg-background/50">
              <div className="flex gap-2">
                <Textarea 
                  placeholder="Post an update to the timeline..."
                  className="min-h-[60px] resize-none"
                  value={updateMsg}
                  onChange={(e) => setUpdateMsg(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handlePostUpdate();
                    }
                  }}
                />
                <Button 
                  className="h-auto" 
                  onClick={handlePostUpdate}
                  disabled={!updateMsg.trim() || createEvent.isPending}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Details Column */}
        <div className="space-y-6 overflow-y-auto">
          <Card>
            <CardHeader>
              <CardTitle>Impact Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="text-sm font-medium text-muted-foreground mb-1">Declared</div>
                <div>{format(new Date(incident.created_at), "MMM d, yyyy HH:mm:ss")}</div>
              </div>
              <div>
                <div className="text-sm font-medium text-muted-foreground mb-1">Commander</div>
                <div>{incident.commander_id || "Unassigned"}</div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Linked Alerts</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-muted-foreground text-center py-4 border border-dashed rounded">
                No alerts explicitly linked.
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
