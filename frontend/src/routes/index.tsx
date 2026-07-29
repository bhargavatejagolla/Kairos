import { createBrowserRouter } from "react-router-dom";
import { AppShell } from "@/layouts/AppShell";
import { AuthLayout } from "@/layouts/AuthLayout";
import { Login } from "@/pages/Login";
import { Dashboard } from "@/pages/Dashboard";
import { Organizations } from "@/pages/Organizations";
import { Projects } from "@/pages/Projects";
import { Services } from "@/pages/Services";
import { Users } from "@/pages/Users";
import { Settings } from "@/pages/Settings";
import { Incidents } from "@/pages/Incidents";
import { IncidentDetails } from "@/pages/IncidentDetails";
import { Alerts } from "@/pages/Alerts";
import { Audit } from "@/pages/Audit";
import { AI } from "@/pages/AI";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: "organizations", element: <Organizations /> },
      { path: "projects", element: <Projects /> },
      { path: "services", element: <Services /> },
      { path: "incidents", element: <Incidents /> },
      { path: "incidents/:id", element: <IncidentDetails /> },
      { path: "alerts", element: <Alerts /> },
      { path: "ai", element: <AI /> },
      { path: "audit", element: <Audit /> },
      { path: "users", element: <Users /> },
      { path: "settings", element: <Settings /> },
    ],
  },
  {
    element: <AuthLayout />,
    children: [
      { path: "login", element: <Login /> },
    ],
  },
]);
