import { useServices } from "@/hooks/useServices";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Plus, Server, GitBranch } from "lucide-react";
import { format } from "date-fns";

export function Services() {
  const { data: services, isLoading, error } = useServices();

  if (isLoading) return <div className="p-8">Loading services...</div>;
  if (error) return <div className="p-8 text-destructive">Failed to load services</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Services</h1>
          <p className="text-muted-foreground mt-2">Manage your microservices and components.</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Register Service
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {services?.map((service) => (
          <Card key={service.id} className="flex flex-col hover:border-primary/50 transition-colors">
            <CardHeader className="pb-4">
              <div className="flex justify-between items-start mb-2">
                <div className="p-2 bg-primary/10 rounded-md">
                  <Server className="h-5 w-5 text-primary" />
                </div>
                <Badge variant={service.tier === "tier-1" ? "destructive" : "secondary"} className="uppercase">
                  {service.tier}
                </Badge>
              </div>
              <CardTitle className="text-xl">{service.name}</CardTitle>
              <CardDescription className="line-clamp-2 h-10 mt-1">
                {service.description || "No description provided for this service."}
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-1 space-y-4">
              {service.repository_url && (
                <div className="flex items-center text-sm text-muted-foreground">
                  <GitBranch className="h-4 w-4 mr-2" />
                  <a href={service.repository_url} target="_blank" rel="noreferrer" className="hover:underline truncate">
                    {service.repository_url}
                  </a>
                </div>
              )}
              <div className="text-xs text-muted-foreground pt-4 border-t border-border">
                Registered on {format(new Date(service.created_at), "MMM d, yyyy")}
              </div>
            </CardContent>
          </Card>
        ))}
        
        {services?.length === 0 && (
          <div className="col-span-full p-12 text-center border border-dashed rounded-lg">
            <Server className="mx-auto h-8 w-8 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No services found</h3>
            <p className="text-muted-foreground mt-1 mb-4">Register your first microservice to start tracking it.</p>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Register Service
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
