import Keycloak from "keycloak-js";

const keycloakConfig = {
  url: process.env.NEXT_PUBLIC_KEYCLOAK_URL || "http://localhost:8080",
  realm: process.env.NEXT_PUBLIC_KEYCLOAK_REALM || "quicktrust",
  clientId: process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID || "quicktrust-web",
};

let keycloakInstance: Keycloak | null = null;

export function getKeycloak(): Keycloak {
  if (!keycloakInstance) {
    keycloakInstance = new Keycloak(keycloakConfig);
  }
  return keycloakInstance;
}

export async function initKeycloak(): Promise<boolean> {
  const kc = getKeycloak();
  try {
    // check-sso: if user has an active Keycloak session, auto-authenticate.
    // If not, return false without redirecting to login page.
    const authenticated = await kc.init({
      onLoad: "check-sso",
      pkceMethod: "S256",
      checkLoginIframe: false,
    });
    return authenticated;
  } catch (error) {
    console.error("Keycloak init failed:", error);
    return false;
  }
}

export function login() {
  const kc = getKeycloak();
  kc.login({ redirectUri: window.location.origin + "/dashboard" });
}

export function logout() {
  const kc = getKeycloak();
  sessionStorage.removeItem("qt_was_auth");
  kc.logout({ redirectUri: window.location.origin });
}

export function getToken(): string | undefined {
  return getKeycloak().token;
}

export async function refreshToken(): Promise<boolean> {
  const kc = getKeycloak();
  try {
    return await kc.updateToken(30);
  } catch {
    return false;
  }
}
