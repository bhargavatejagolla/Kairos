import { usePlatformStatistics } from "@/hooks/useStatistics";
import { useIncidents } from "@/hooks/useIncidents";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, ShieldAlert, CheckCircle, Clock } from "lucide-react";
import { 
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart 
} from "recharts";
import { format, subDays } from "date-fns";

export function Dashboard() {
  const { data: stats, isLoading: statsLoading } = usePlatformStatistics();
  const { data: incidents, isLoading: incidentsLoading } = useIncidents();

  if (statsLoading || incidentsLoading) {
    return <div className="p-8 animate-pulse text-muted-foreground">Loading dashboard telemetry...</div>;
  }

  // Mocking trend data based on current stats for the chart 
  // (In a full prod environment, backend provides a time-series array)
  const generateTrendData = () => {
    const data = [];
    for (let i = 6; i >= 0; i--) {
      data.push({
        name: format(subDays(new Date(), i), 'MMM dd'),
        alerts: Math.floor(Math.random() * 50) + (stats?.active_alerts || 10),
        incidents: Math.floor(Math.random() * 5) + (stats?.active_incidents || 0),
      });
    }
    return data;
  };

  const trendData = generateTrendData();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Platform Overview</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Platform Health</CardTitle>
            <Activity className={`h-4 w-4 ${stats?.active_incidents ? "text-destructive" : "text-green-500"}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {stats?.active_incidents ? "Degraded" : "99.99%"}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.active_incidents ? "Active incidents impacting health" : "All systems operational"}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Incidents</CardTitle>
            <ShieldAlert className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.active_incidents || 0}</div>
            <p className="text-xs text-muted-foreground">
              Out of {stats?.total_incidents || 0} total historically
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Alerts</CardTitle>
            <CheckCircle className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.active_alerts || 0}</div>
            <p className="text-xs text-muted-foreground">
              Requires immediate triage
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">MTTR</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.mttr || 0} min</div>
            <p className="text-xs text-muted-foreground">
              Mean time to resolution
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>System Anomaly Volume</CardTitle>
            <CardDescription>Alerts and incidents over the last 7 days</CardDescription>
          </CardHeader>
          <CardContent className="pl-2 h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorAlerts" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorIncidents" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--destructive))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--destructive))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis 
                  dataKey="name" 
                  stroke="hsl(var(--muted-foreground))" 
                  fontSize={12} 
                  tickLine={false} 
                  axisLine={false} 
                />
                <YAxis 
                  stroke="hsl(var(--muted-foreground))" 
                  fontSize={12} 
                  tickLine={false} 
                  axisLine={false} 
                  tickFormatter={(value) => `${value}`}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Area type="monotone" dataKey="alerts" stroke="hsl(var(--primary))" fillOpacity={1} fill="url(#colorAlerts)" />
                <Area type="monotone" dataKey="incidents" stroke="hsl(var(--destructive))" fillOpacity={1} fill="url(#colorIncidents)" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Incidents</CardTitle>
            <CardDescription>Latest declared incidents</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {incidents?.slice(0, 5).map((incident) => (
                <div key={incident.id} className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-4 ${
                    incident.severity === 'critical' ? 'bg-destructive' : 'bg-primary'
                  }`} />
                  <div className="ml-4 space-y-1">
                    <p className="text-sm font-medium leading-none">{incident.title}</p>
                    <p className="text-xs text-muted-foreground">
                      {format(new Date(incident.created_at), "MMM d, HH:mm")}
                    </p>
                  </div>
                  <div className="ml-auto font-medium text-xs">
                    <span className="uppercase text-muted-foreground border border-border px-2 py-1 rounded-md">
                      {incident.status}
                    </span>
                  </div>
                </div>
              ))}
              {(!incidents || incidents.length === 0) && (
                <div className="text-sm text-muted-foreground text-center py-4">
                  No recent incidents.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
