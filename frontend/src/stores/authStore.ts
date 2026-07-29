import { create } from "zustand";

interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem("kairos_auth_token") || null,
  isAuthenticated: !!localStorage.getItem("kairos_auth_token"),
  login: (token, user) => {
    localStorage.setItem("kairos_auth_token", token);
    set({ user, token, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem("kairos_auth_token");
    set({ user: null, token: null, isAuthenticated: false });
  },
}));
