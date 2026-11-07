export type ActionClass = "read" | "draft" | "external" | "restricted";
export type TaskStatus = "open" | "approval_required" | "approved" | "rejected" | "completed";

export interface AtlasTask {
  id: string;
  title: string;
  description?: string;
  action_class: ActionClass;
  status: TaskStatus;
  requested_by: string;
  approved_by?: string;
  decision_note?: string;
  created_at: string;
  updated_at: string;
  version: number;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  action_class: ActionClass;
}

export class AtlasClient {
  private readonly baseUrl: string;
  constructor(baseUrl: string, private readonly token: string) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    if (!this.token) throw new Error("ATLAS API token is required");
  }

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        "Authorization": `Bearer ${this.token}`,
        "Content-Type": "application/json",
        ...init.headers,
      },
    });
    const payload: unknown = await response.json();
    if (!response.ok) {
      const message = typeof payload === "object" && payload !== null && "error" in payload
        ? String((payload as { error: unknown }).error)
        : `ATLAS API error ${response.status}`;
      throw new Error(message);
    }
    return payload as T;
  }

  async listTasks(): Promise<AtlasTask[]> {
    const result = await this.request<{ tasks: AtlasTask[] }>("/v1/tasks");
    return result.tasks;
  }

  async createTask(input: CreateTaskInput): Promise<AtlasTask> {
    return this.request<AtlasTask>("/v1/tasks", { method: "POST", body: JSON.stringify(input) });
  }

  async approveTask(id: string, decision: "approve" | "reject", reason = ""): Promise<AtlasTask> {
    return this.request<AtlasTask>(`/v1/tasks/${encodeURIComponent(id)}/approval`, {
      method: "POST", body: JSON.stringify({ decision, reason }),
    });
  }

  async completeTask(id: string): Promise<AtlasTask> {
    return this.request<AtlasTask>(`/v1/tasks/${encodeURIComponent(id)}/complete`, { method: "POST" });
  }
}
