import { useAuditLogs } from "@/hooks/useAudit";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Shield, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { format } from "date-fns";

export function Audit() {
  const { data: logs, isLoading, error } = useAuditLogs();

  if (isLoading) return <div className="p-8">Loading audit logs...</div>;
  if (error) return <div className="p-8 text-destructive">Failed to load audit logs</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Shield className="h-8 w-8 text-primary" />
            Audit Logs
          </h1>
          <p className="text-muted-foreground mt-2">Immutable record of all platform actions and security events.</p>
        </div>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>System Activity</CardTitle>
            <CardDescription>Chronological log of changes.</CardDescription>
          </div>
          <div className="w-72 relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input placeholder="Search logs..." className="pl-8" />
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Timestamp</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>Resource Type</TableHead>
                <TableHead>Actor IP</TableHead>
                <TableHead className="text-right">Details</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {logs?.map((log) => (
                <TableRow key={log.id}>
                  <TableCell className="text-sm font-mono text-muted-foreground">
                    {format(new Date(log.created_at), "yyyy-MM-dd HH:mm:ss")}
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="font-mono bg-secondary/50">
                      {log.action}
                    </Badge>
                  </TableCell>
                  <TableCell className="capitalize">{log.resource_type}</TableCell>
                  <TableCell className="text-sm text-muted-foreground">{log.ip_address || "unknown"}</TableCell>
                  <TableCell className="text-right text-xs text-muted-foreground font-mono truncate max-w-[200px]">
                    {JSON.stringify(log.details)}
                  </TableCell>
                </TableRow>
              ))}
              {logs?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                    No audit logs available.
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
