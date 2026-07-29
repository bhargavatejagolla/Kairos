import { useAlerts, useAcknowledgeAlert } from "@/hooks/useAlerts";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AlertTriangle, CheckCircle, BellRing } from "lucide-react";
import { format } from "date-fns";

export function Alerts() {
  const { data: alerts, isLoading, error } = useAlerts();
  const acknowledgeAlert = useAcknowledgeAlert();

  if (isLoading) return <div className="p-8">Loading alerts...</div>;
  if (error) return <div className="p-8 text-destructive">Failed to load alerts</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <BellRing className="h-8 w-8 text-primary" />
            Alerts & Signals
          </h1>
          <p className="text-muted-foreground mt-2">Real-time monitoring feed of system anomalies.</p>
        </div>
      </div>

      <div className="grid gap-4">
        {alerts?.map((alert) => (
          <Card key={alert.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-6">
            <div className="flex items-start gap-4">
              <div className={`p-2 rounded-full mt-1 ${alert.severity === 'critical' ? 'bg-destructive/10 text-destructive' : 'bg-primary/10 text-primary'}`}>
                <AlertTriangle className="h-6 w-6" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-lg">{alert.title}</h3>
                  <Badge variant={alert.severity === "critical" ? "destructive" : "secondary"}>
                    {alert.severity}
                  </Badge>
                  <Badge variant="outline">{alert.status}</Badge>
                </div>
                <p className="text-sm text-muted-foreground mb-2">{alert.description}</p>
                <div className="text-xs text-muted-foreground">
                  Source: {alert.source} • Detected: {format(new Date(alert.created_at), "MMM d, HH:mm:ss")}
                </div>
              </div>
            </div>
            
            <div className="mt-4 sm:mt-0 flex gap-2">
              {alert.status === "firing" && (
                <>
                  <Button 
                    variant="outline"
                    onClick={() => acknowledgeAlert.mutate(alert.id)}
                    disabled={acknowledgeAlert.isPending}
                  >
                    <CheckCircle className="mr-2 h-4 w-4" />
                    Acknowledge
                  </Button>
                  <Button variant="destructive">Escalate to Incident</Button>
                </>
              )}
            </div>
          </Card>
        ))}
        {alerts?.length === 0 && (
          <div className="p-12 text-center border border-dashed rounded-lg">
            <CheckCircle className="mx-auto h-8 w-8 text-green-500 mb-4" />
            <h3 className="text-lg font-medium">All clear</h3>
            <p className="text-muted-foreground mt-1">No active alerts right now.</p>
          </div>
        )}
      </div>
    </div>
  );
}
