import { Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-foreground">KAIROS</h1>
          <p className="text-muted-foreground mt-2 text-sm">Enterprise Operations Console</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
}
