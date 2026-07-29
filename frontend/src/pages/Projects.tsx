import { useProjects } from "@/hooks/useProjects";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, FolderGit2 } from "lucide-react";
import { format } from "date-fns";

export function Projects() {
  const { data: projects, isLoading, error } = useProjects();

  if (isLoading) return <div className="p-8">Loading projects...</div>;
  if (error) return <div className="p-8 text-destructive">Failed to load projects</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Projects</h1>
          <p className="text-muted-foreground mt-2">Manage your projects and resources.</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Create Project
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {projects?.map((project) => (
          <Card key={project.id} className="flex flex-col hover:border-primary/50 transition-colors cursor-pointer">
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <div className="p-2 bg-primary/10 rounded-md">
                  <FolderGit2 className="h-5 w-5 text-primary" />
                </div>
              </div>
              <CardTitle>{project.name}</CardTitle>
              <CardDescription className="line-clamp-2">
                {project.description || "No description provided."}
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-1">
              <div className="text-sm text-muted-foreground mt-2">
                Created {format(new Date(project.created_at), "MMM d, yyyy")}
              </div>
            </CardContent>
            <CardFooter className="border-t border-border pt-4">
              <Button variant="outline" className="w-full">View Services</Button>
            </CardFooter>
          </Card>
        ))}
        {projects?.length === 0 && (
          <div className="col-span-full p-12 text-center border border-dashed rounded-lg">
            <FolderGit2 className="mx-auto h-8 w-8 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No projects found</h3>
            <p className="text-muted-foreground mt-1 mb-4">Get started by creating a new project.</p>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Project
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
