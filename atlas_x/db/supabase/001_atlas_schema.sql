-- Supabase-specific schema: requires Supabase Auth and auth.uid().
create schema if not exists atlas;

create table if not exists atlas.workspaces (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 1 and 160),
  created_at timestamptz not null default now()
);

create table if not exists atlas.workspace_memberships (
  workspace_id uuid not null references atlas.workspaces(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null check (role in ('owner','admin','member','viewer')),
  created_at timestamptz not null default now(),
  primary key (workspace_id, user_id)
);

create table if not exists atlas.tasks (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references atlas.workspaces(id) on delete cascade,
  title text not null check (char_length(title) between 1 and 200),
  description text not null default '' check (char_length(description) <= 8000),
  action_class text not null check (action_class in ('read','draft','external','restricted')),
  status text not null check (status in ('open','approval_required','approved','rejected','completed')),
  version bigint not null default 1 check (version > 0),
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists atlas.approvals (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references atlas.workspaces(id) on delete cascade,
  task_id uuid not null references atlas.tasks(id) on delete cascade,
  decision text not null check (decision in ('approve','reject')),
  reason text not null default '' check (char_length(reason) <= 1000),
  decided_by uuid not null references auth.users(id),
  decided_at timestamptz not null default now()
);

create table if not exists atlas.audit_events (
  id bigint generated always as identity primary key,
  workspace_id uuid not null references atlas.workspaces(id) on delete cascade,
  actor_id uuid references auth.users(id),
  event_type text not null,
  aggregate_type text not null,
  aggregate_id uuid not null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists tasks_workspace_created_idx on atlas.tasks(workspace_id, created_at desc);
create index if not exists audit_workspace_created_idx on atlas.audit_events(workspace_id, created_at desc);

alter table atlas.workspaces enable row level security;
alter table atlas.workspace_memberships enable row level security;
alter table atlas.tasks enable row level security;
alter table atlas.approvals enable row level security;
alter table atlas.audit_events enable row level security;

create policy workspace_member_select on atlas.workspaces for select
  using (exists (select 1 from atlas.workspace_memberships m where m.workspace_id = id and m.user_id = auth.uid()));
create policy membership_self_select on atlas.workspace_memberships for select
  using (user_id = auth.uid());
create policy tasks_member_select on atlas.tasks for select
  using (exists (select 1 from atlas.workspace_memberships m where m.workspace_id = workspace_id and m.user_id = auth.uid()));
create policy tasks_member_insert on atlas.tasks for insert
  with check (created_by = auth.uid() and exists (select 1 from atlas.workspace_memberships m where m.workspace_id = workspace_id and m.user_id = auth.uid()));
create policy tasks_member_update on atlas.tasks for update
  using (exists (select 1 from atlas.workspace_memberships m where m.workspace_id = workspace_id and m.user_id = auth.uid() and m.role in ('owner','admin','member')))
  with check (exists (select 1 from atlas.workspace_memberships m where m.workspace_id = workspace_id and m.user_id = auth.uid() and m.role in ('owner','admin','member')));
create policy approvals_member_select on atlas.approvals for select
  using (exists (select 1 from atlas.workspace_memberships m where m.workspace_id = workspace_id and m.user_id = auth.uid()));
create policy audit_member_select on atlas.audit_events for select
  using (exists (select 1 from atlas.workspace_memberships m where m.workspace_id = workspace_id and m.user_id = auth.uid()));

-- Production hardening required: privileged writes should use narrow server-side RPC/service logic;
-- audit_events should be append-only to application roles, with no UPDATE or DELETE grants.
