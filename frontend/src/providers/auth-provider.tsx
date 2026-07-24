"use client";

import React, { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import api from "@/lib/api";
import {
  AuthUser,
  fetchCurrentUser,
  refreshSession,
  registerAccount,
  revokeSession,
  signIn,
  TokenResponse,
} from "@/lib/auth";

interface UserInfo {
  id: string | null;
  name: string;
  email: string;
  role: string;
  roles: string[];
  org_id: string | null;
}

interface AuthContextType {
  authenticated: boolean;
  loading: boolean;
  token: string | null;
  userInfo: UserInfo | null;
  login: (returnTo?: string, email?: string) => void;
  signIn: (email: string, password: string) => Promise<void>;
  register: (input: {
    email: string;
    full_name: string;
    password: string;
    invitation_token?: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  authenticated: false,
  loading: true,
  token: null,
  userInfo: null,
  login: () => {},
  signIn: async () => {},
  register: async () => {},
  logout: async () => {},
});

function toUserInfo(user: AuthUser): UserInfo {
  return {
    id: user.id,
    name: user.full_name,
    email: user.email,
    role: user.role,
    roles: [user.role],
    org_id: user.org_id,
  };
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const tokenRef = useRef<string | null>(null);
  const refreshInFlight = useRef<Promise<string | null> | null>(null);

  const clearSession = useCallback(() => {
    tokenRef.current = null;
    api.setToken(null);
    setToken(null);
    setUserInfo(null);
    setAuthenticated(false);
  }, []);

  const applySession = useCallback(async (session: TokenResponse) => {
    const accessToken = session.access_token;
    tokenRef.current = accessToken;
    api.setToken(accessToken);
    const user = await fetchCurrentUser(accessToken);
    setToken(accessToken);
    setUserInfo(toUserInfo(user));
    setAuthenticated(true);
    return accessToken;
  }, []);

  const refresh = useCallback(async (): Promise<string | null> => {
    if (refreshInFlight.current) return refreshInFlight.current;
    refreshInFlight.current = refreshSession()
      .then(applySession)
      .catch(() => {
        clearSession();
        return null;
      })
      .finally(() => {
        refreshInFlight.current = null;
      });
    return refreshInFlight.current;
  }, [applySession, clearSession]);

  useEffect(() => {
    let active = true;
    refresh().finally(() => {
      if (active) setLoading(false);
    });
    const refreshTimer = window.setInterval(refresh, 12 * 60 * 1000);
    api.setRefreshHandler(refresh);
    return () => {
      active = false;
      window.clearInterval(refreshTimer);
      api.setRefreshHandler(null);
    };
  }, [refresh]);

  const doSignIn = useCallback(
    async (email: string, password: string) => {
      try {
        await applySession(await signIn(email, password));
      } catch (error) {
        clearSession();
        throw error;
      }
    },
    [applySession, clearSession]
  );

  const doRegister = useCallback(
    async (input: {
      email: string;
      full_name: string;
      password: string;
      invitation_token?: string;
    }) => {
      try {
        await applySession(await registerAccount(input));
      } catch (error) {
        clearSession();
        throw error;
      }
    },
    [applySession, clearSession]
  );

  const login = useCallback((returnTo?: string, email?: string) => {
    const params = new URLSearchParams();
    if (returnTo) params.set("returnTo", returnTo);
    if (email) params.set("email", email);
    window.location.assign(`/login${params.size ? `?${params}` : ""}`);
  }, []);

  const logout = useCallback(async () => {
    const currentToken = tokenRef.current;
    try {
      if (currentToken) await revokeSession(currentToken);
    } finally {
      clearSession();
      window.location.assign("/login");
    }
  }, [clearSession]);

  return (
    <AuthContext.Provider
      value={{
        authenticated,
        loading,
        token,
        userInfo,
        login,
        signIn: doSignIn,
        register: doRegister,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
