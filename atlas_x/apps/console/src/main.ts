import { AtlasClient, type AtlasTask, type ActionClass } from "../../../packages/typescript-sdk/src/index.js";

const $ = <T extends HTMLElement>(id: string): T => {
  const node = document.getElementById(id);
  if (!node) throw new Error(`Missing UI element: ${id}`);
  return node as T;
};

let client: AtlasClient | null = null;
const status = $("status");
const taskRoot = $("tasks");

function setStatus(message: string): void { status.textContent = message; }
function escapeText(value: string): string {
  return value.replace(/[&<>"']/g, (char) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" })[char] ?? char);
}

function renderTasks(tasks: AtlasTask[]): void {
  taskRoot.innerHTML = "";
  if (tasks.length === 0) { taskRoot.textContent = "No tasks yet."; return; }
  for (const task of tasks) {
    const row = document.createElement("div");
    row.className = "task";
    const content = document.createElement("div");
    const title = document.createElement("strong"); title.textContent = task.title;
    const detail = document.createElement("p"); detail.className = "muted";
    detail.textContent = `${task.action_class} · ${task.status} · v${task.version}`;
    const id = document.createElement("code"); id.textContent = task.id;
    content.append(title, detail, id);
    const controls = document.createElement("div");
    if (task.status === "approval_required") {
      const approve = document.createElement("button"); approve.textContent = "Approve";
      approve.addEventListener("click", () => void act(async () => { await client?.approveTask(task.id, "approve", "Approved in local console"); await refresh(); }));
      const reject = document.createElement("button"); reject.className = "secondary"; reject.textContent = "Reject";
      reject.addEventListener("click", () => void act(async () => { await client?.approveTask(task.id, "reject", "Rejected in local console"); await refresh(); }));
      controls.append(approve, reject);
    } else if (task.status === "open" || task.status === "approved") {
      const complete = document.createElement("button"); complete.textContent = "Mark complete";
      complete.addEventListener("click", () => void act(async () => { await client?.completeTask(task.id); await refresh(); }));
      controls.append(complete);
    }
    row.append(content, controls); taskRoot.append(row);
  }
}

async function act(operation: () => Promise<void>): Promise<void> {
  try { await operation(); setStatus("Operation completed."); }
  catch (error) { setStatus(error instanceof Error ? error.message : "Operation failed"); }
}

async function refresh(): Promise<void> {
  if (!client) { setStatus("Connect first."); return; }
  const tasks = await client.listTasks(); renderTasks(tasks);
}

$("connect").addEventListener("click", () => void act(async () => {
  const token = $("token" as string as "token").value;
  const api = $("api" as string as "api").value;
  client = new AtlasClient(api, token);
  await refresh();
  setStatus("Connected. Token remains in this page memory only.");
}));

$("create").addEventListener("click", () => void act(async () => {
  if (!client) throw new Error("Connect first.");
  const title = $("title").value.trim();
  const description = $("description").value.trim();
  const actionClass = $("class").value as ActionClass;
  if (!title) throw new Error("Enter a task title.");
  await client.createTask({ title, description, action_class: actionClass });
  $("title").value = ""; $("description").value = "";
  await refresh();
}));

$("refresh").addEventListener("click", () => void act(refresh));
