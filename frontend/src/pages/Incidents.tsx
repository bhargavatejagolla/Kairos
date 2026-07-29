import { useIncidents } from "@/hooks/useIncidents";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Plus, Flame } from "lucide-react";
import { format } from "date-fns";

export function Incidents() {
  const { data: incidents, isLoading, error } = useIncidents();

  if (isLoading) return <div className="p-8">Loading incidents...</div>;
  if (error) return <div className="p-8 text-destructive">Failed to load incidents</div>;

  const getSeverityVariant = (severity: string) => {
    switch (severity) {
      case "critical": return "destructive";
      case "high": return "default";
      case "medium": return "secondary";
      case "low": return "outline";
      default: return "outline";
    }
  };

  const getStatusVariant = (status: string) => {
    switch (status) {
      case "investigating": return "destructive";
      case "identified": return "secondary";
      case "monitoring": return "outline";
      case "resolved": return "default";
      default: return "outline";
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Flame className="h-8 w-8 text-destructive" />
            Incidents
          </h1>
          <p className="text-muted-foreground mt-2">Manage ongoing and past incidents across the platform.</p>
        </div>
        <Button variant="destructive">
          <Plus className="mr-2 h-4 w-4" />
          Declare Incident
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Active & Recent Incidents</CardTitle>
          <CardDescription>A complete log of all critical events.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Severity</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Declared At</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {incidents?.map((incident) => (
                <TableRow key={incident.id}>
                  <TableCell className="font-medium">{incident.title}</TableCell>
                  <TableCell>
                    <Badge variant={getSeverityVariant(incident.severity)} className="uppercase">
                      {incident.severity}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={getStatusVariant(incident.status)} className="capitalize">
                      {incident.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {format(new Date(incident.created_at), "MMM d, yyyy HH:mm")}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" asChild>
                      <Link to={`/incidents/${incident.id}`}>War Room</Link>
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
              {incidents?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                    No incidents reported. All systems optimal.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
