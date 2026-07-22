import { API_URL } from "@/lib/public-env";

type QueryParamValue = string | number | boolean | null | undefined;

interface ApiRequestOptions extends RequestInit {
  params?: Record<string, QueryParamValue>;
}


class ApiClient {
  private baseUrl: string;
  private token: string | null = null;
  private refreshHandler: (() => Promise<string | null>) | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  setToken(token: string | null) {
    this.token = token;
  }

  setRefreshHandler(handler: (() => Promise<string | null>) | null) {
    this.refreshHandler = handler;
  }

  private async request<T>(
    path: string,
    options: ApiRequestOptions = {}
  ): Promise<T> {
    const { params, ...requestOptions } = options;
    const url = new URL(`${this.baseUrl}${path}`);
    Object.entries(params ?? {}).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        url.searchParams.set(key, String(value));
      }
    });

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...((requestOptions.headers as Record<string, string>) ?? {}),
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    let res = await fetch(url.toString(), {
      ...requestOptions,
      credentials: "include",
      headers,
    });

    if (res.status === 401 && this.refreshHandler) {
      const refreshedToken = await this.refreshHandler();
      if (refreshedToken) {
        headers["Authorization"] = `Bearer ${refreshedToken}`;
        res = await fetch(url.toString(), {
          ...requestOptions,
          credentials: "include",
          headers,
        });
      }
    }

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: res.statusText }));
      // FastAPI validation errors return detail as an array of objects
      const detail = error.detail;
      let message: string;
      if (Array.isArray(detail)) {
        message = detail.map((d: any) => d.msg || JSON.stringify(d)).join("; ");
      } else if (typeof detail === "string") {
        message = detail;
      } else {
        message = `API error: ${res.status}`;
      }
      throw new Error(message);
    }

    if (res.status === 204) return undefined as T;
    return res.json();
  }

  get<T>(path: string, options?: ApiRequestOptions) {
    return this.request<T>(path, options);
  }

  post<T>(path: string, body?: unknown) {
    return this.request<T>(path, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  put<T>(path: string, body: unknown) {
    return this.request<T>(path, {
      method: "PUT",
      body: JSON.stringify(body),
    });
  }

  patch<T>(path: string, body: unknown) {
    return this.request<T>(path, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
  }

  delete(path: string) {
    return this.request(path, { method: "DELETE" });
  }

  async downloadRedirect(path: string): Promise<void> {
    const headers: Record<string, string> = {};
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }
    const res = await fetch(`${this.baseUrl}${path}`, {
      headers,
      credentials: "include",
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(error.detail || `Download error: ${res.status}`);
    }
    const blob = await res.blob();
    // Extract filename from Content-Disposition header
    const disposition = res.headers.get("Content-Disposition");
    let filename = "download";
    if (disposition) {
      const match = disposition.match(/filename="?([^";\n]+)"?/);
      if (match) filename = match[1];
    }
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  async upload<T>(path: string, file: File, fieldName: string = "file"): Promise<T> {
    const formData = new FormData();
    formData.append(fieldName, file);

    const headers: Record<string, string> = {};
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }
    // Do NOT set Content-Type — browser sets it with boundary for multipart

    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers,
      body: formData,
      credentials: "include",
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(error.detail || `Upload error: ${res.status}`);
    }

    return res.json();
  }
}

export const api = new ApiClient(`${API_URL}/api/v1`);
export default api;
