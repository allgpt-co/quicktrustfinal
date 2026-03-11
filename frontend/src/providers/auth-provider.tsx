"use client";

import React, {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import api from "@/lib/api";

interface AuthContextType {
  authenticated: boolean;
  loading: boolean;
  token: string | null;
  userInfo: {
    name: string;
    email: string;
    role: string;
    roles: string[];
    org_id: string | null;
  } | null;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  authenticated: false,
  loading: true,
  token: null,
  userInfo: null,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [authenticated, setAuthenticated] = useState(false);
  // Start with loading=true to avoid hydration mismatch (server and client
  // must render the same initial HTML). Resolved in the useEffect below.
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState<AuthContextType["userInfo"]>(null);
  const initDone = useRef(false);

  useEffect(() => {
    if (initDone.current) return;
    initDone.current = true;

    // Timeout: never hang on loading longer than 6 seconds
    const timeout = new Promise<boolean>((resolve) =>
      setTimeout(() => resolve(false), 6000)
    );

    import("@/lib/auth").then(({ initKeycloak, getKeycloak }) => {
      Promise.race([initKeycloak(), timeout])
        .then(async (auth) => {
          setAuthenticated(auth);

          if (auth) {
            // Remember user was logged in so next refresh shows spinner
            sessionStorage.setItem("qt_was_auth", "1");

            const kc = getKeycloak();
            const t = kc.token || null;
            setToken(t);
            api.setToken(t);

            let orgId: string | null = kc.tokenParsed?.org_id || null;
            let backendRole: string = "employee";
            try {
              const res = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/me`,
                { headers: { Authorization: `Bearer ${t}` } }
              );
              if (res.ok) {
                const me = await res.json();
                orgId = me.org_id || orgId;
                backendRole = me.role || backendRole;
              }
            } catch {
              // fall back to token org_id
            }

            setUserInfo({
              name: kc.tokenParsed?.name || kc.tokenParsed?.preferred_username || "",
              email: kc.tokenParsed?.email || "",
              role: backendRole,
              roles: kc.tokenParsed?.realm_roles || [],
              org_id: orgId,
            });

            setInterval(async () => {
              try {
                await kc.updateToken(30);
                const newToken = kc.token || null;
                setToken(newToken);
                api.setToken(newToken);
              } catch {
                setAuthenticated(false);
                sessionStorage.removeItem("qt_was_auth");
              }
            }, 60000);
          } else {
            // Not authenticated — clear the flag so next visit is instant
            sessionStorage.removeItem("qt_was_auth");
          }

          setLoading(false);
        })
        .catch(() => {
          sessionStorage.removeItem("qt_was_auth");
          setLoading(false);
        });
    });
  }, []);

  const doLogin = () => {
    import("@/lib/auth").then(({ login }) => login());
  };

  const doLogout = () => {
    import("@/lib/auth").then(({ logout }) => logout());
  };

  return (
    <AuthContext.Provider
      value={{ authenticated, loading, token, userInfo, login: doLogin, logout: doLogout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
