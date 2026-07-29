import { Outlet, Navigate, Link } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";
import { LogOut, LayoutDashboard, AlertCircle, Cpu, ShieldAlert, FileText, Settings, Users, FolderGit2, Server, Building2 } from "lucide-react";

export function AppShell() {
  const { isAuthenticated, user, logout } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const navigation = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "Organizations", href: "/organizations", icon: Building2 },
    { name: "Projects", href: "/projects", icon: FolderGit2 },
    { name: "Services", href: "/services", icon: Server },
    { name: "Incidents", href: "/incidents", icon: ShieldAlert },
    { name: "Alerts", href: "/alerts", icon: AlertCircle },
    { name: "AI Workspace", href: "/ai", icon: Cpu },
    { name: "Audit", href: "/audit", icon: FileText },
    { name: "Users", href: "/users", icon: Users },
    { name: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card/50 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-border">
          <h1 className="text-xl font-bold tracking-tight text-foreground">KAIROS</h1>
        </div>
        
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className="flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
              >
                <Icon className="w-4 h-4" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-border flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-sm font-medium">{user?.firstName} {user?.lastName}</span>
            <span className="text-xs text-muted-foreground truncate w-32">{user?.email}</span>
          </div>
          <button 
            onClick={logout}
            className="p-2 rounded-md hover:bg-secondary text-muted-foreground hover:text-foreground"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 border-b border-border flex items-center justify-between px-8 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <h2 className="text-lg font-semibold">Overview</h2>
          {/* Top nav actions like search, notifications will go here */}
        </header>
        <div className="flex-1 overflow-auto p-8">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </div>
      </main>
    </div>
  );
}
