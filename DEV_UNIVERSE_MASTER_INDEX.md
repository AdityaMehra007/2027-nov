# OmniDev Universe: Universal Developer Knowledge & Resource Index

A unified, full-text searchable intelligence engine aggregating over **10,189+ verified developer resources** across 7 premier ecosystems:
1. **[`awesome-selfhosted`](https://github.com/awesome-selfhosted/awesome-selfhosted)** — Free and open-source self-hostable network services, web applications, and SaaS alternatives.
2. **[`developer-roadmap`](https://github.com/nilbuild/developer-roadmap)** — Community-driven career paths, technical skill trees, and interactive developer roadmaps.
3. **[`awesome-python`](https://github.com/vinta/awesome-python)** — The authoritative curated guide to Python frameworks, libraries, AI agents, and tools.
4. **[`free-programming-books`](https://github.com/EbookFoundation/free-programming-books)** — Free books, courses, screencasts, cheatsheets, and interactive tutorials.
5. **[`build-your-own-x`](https://github.com/codecrafters-io/build-your-own-x)** — Step-by-step guides for recreating core technologies from scratch.
6. **[`public-apis`](https://github.com/public-apis/public-apis)** — Public web APIs categorized with authentication, HTTPS, and CORS metadata.
7. **[`awesome`](https://github.com/sindresorhus/awesome)** — Curated lists of frameworks, platforms, and programming topics.

---

## 1. Knowledge Metrics & Coverage

| Metric | Count | Details |
| :--- | :--- | :--- |
| **Total Curated Resources** | **10,189** | Deduplicated across all 7 repositories |
| **Programming & Domain Books** | **2,521** | Languages (Python, Rust, C++, Go, etc.) & Subjects (AI, Security, Math) |
| **Public Web APIs** | **2,380** | 50+ categories with auth & HTTPS specifications |
| **Self-Hosted Applications** | **1,359** | 1,266 Open-Source + 93 Proprietary self-hostable services |
| **Online Video Courses** | **1,343** | Free structured curricula and video courses |
| **Awesome Curated Lists** | **662** | Community-verified ecosystems and toolchains |
| **Python Libraries & Tools** | **538** | AI agents, web frameworks, async, ORM, data science, testing |
| **"Build Your Own" Guides** | **362** | Compilers, Git, OS, Databases, Neural Nets, BitTorrent, Docker |
| **Cheatsheets & References** | **324** | Syntax, shell, tools, frameworks |
| **Podcasts & Screencasts** | **263** | Tech talks, audio deep-dives, developer interviews |
| **Interactive Tutorials** | **210** | In-browser exercises and interactive coding |
| **Competitive Problem Sets** | **126** | Algorithm challenges and competitive programming |
| **Developer Roadmaps** | **96** | AI, Backend, Frontend, DevOps, Security, Cloud, System Design |
| **Newsletters & Websites** | **5** | Curated periodic publications and portals |

---

## 2. Self-Hosted Software & SaaS Replacements Matrix

The `awesome-selfhosted` index provides open-source alternatives to commercial SaaS solutions:

| Commercial SaaS | Open-Source Alternative | Category | Tech Stack | License |
| :--- | :--- | :--- | :--- | :--- |
| **Google Drive / Dropbox** | **Nextcloud Hub** / **Seafile** | Cloud Storage & Collaboration | PHP / Docker / C | AGPL-3.0 |
| **1Password / Bitwarden** | **Vaultwarden** | Password Management | Rust / Docker | AGPL-3.0 |
| **Google Analytics** | **Umami** / **Plausible** / **Matomo** | Privacy Analytics | Node.js / Elixir / PHP | MIT / AGPL |
| **Notion / Coda** | **AppFlowy** / **Atomic Server** | Notes & Workspaces | Rust / Dart / Docker | AGPL-3.0 |
| **Slack / Teams** | **Mattermost** / **Zulip** / **Element** | Team Communication | Go / Python / Matrix | AGPL-3.0 |
| **Zapier / Make** | **n8n** / **Activepieces** / **Automatisch** | Workflow Automation | Node.js / Docker | Fair-Code / MIT |
| **StatusPage / Pingdom** | **Uptime Kuma** | Monitoring & Alerts | Node.js / SQLite | MIT |
| **Jira / Linear** | **Plane** / **Taiga** / **Focalboard** | Issue & Project Tracking | Python / React / Go | AGPL-3.0 |
| **GitHub / GitLab** | **Gitea** / **Forgejo** | Source Code & CI/CD | Go / Docker | MIT |
| **Substack / Medium** | **Ghost** | Publishing & Newsletters | Node.js / MySQL | MIT |
| **Algolia / Elasticsearch** | **Meilisearch** / **Typesense** | Search Engines | Rust / C++ / Docker | MIT / Apache-2.0 |
| **DocuSign / Paperwork** | **Paperless-ngx** | Document Management & OCR | Python / Django / Docker | GPL-3.0 |

---

## 3. Production Self-Hosted Launcher (`scripts/selfhosted_launcher.py`)

Generate production-grade Docker Compose stacks with automated random secrets, volume persistence, and optional Caddy reverse-proxy SSL configurations with a single command:

```powershell
# List available production stacks
python scripts/selfhosted_launcher.py list

# Inspect stack details and required ports
python scripts/selfhosted_launcher.py info nextcloud

# Generate Nextcloud stack in deploy/selfhosted/nextcloud
python scripts/selfhosted_launcher.py generate nextcloud

# Generate Vaultwarden stack with automated Caddy SSL for custom domain
python scripts/selfhosted_launcher.py generate vaultwarden --with-caddy --domain vault.homelab.local

# Generate n8n workflow automation stack
python scripts/selfhosted_launcher.py generate n8n
```

---

## 4. Developer Career & Technical Roadmaps (`developer-roadmap`)

Community-verified step-by-step guides and skill trees covering:
- **AI & Modern Engineering**: AI Agents, AI Engineer, AI Data Scientist, AI Product Builder, AI Red Teaming, Inference Engineering, Prompt Engineering.
- **Foundations & Core Roles**: Backend Developer, Frontend Developer, DevOps Engineer, Full Stack, Software Architect, System Design.
- **Cloud & Infrastructure**: AWS, Azure, Cloud Computing, Cloudflare, Docker, Kubernetes, Terraform.
- **Security & Quality**: Cyber Security, DevSecOps, Code Review, QA Engineer.
- **Language Deep-Dives**: Python, Rust, Go, TypeScript, C++, Kotlin, Java, PHP, Ruby.

---

## 5. Fast CLI Search Engine (`scripts/search_dev_universe.py`)

Search directly in your terminal:

### Find SaaS Replacements
```powershell
# Find self-hosted alternatives to Notion
python scripts/search_dev_universe.py -S notion

# Find self-hosted alternatives to Slack
python scripts/search_dev_universe.py -S slack

# Find self-hosted alternatives to Google Analytics
python scripts/search_dev_universe.py -S google-analytics
```

### Filter by Resource Type
Available types: `self-hosted`, `roadmap`, `library`, `book`, `course`, `build-project`, `api`, `cheatsheet`, `interactive`, `podcast`, `curated-list`, `problem-set`

```powershell
# Search self-hosted backup tools
python scripts/search_dev_universe.py -q "backup" -t self-hosted

# Search AI agent roadmaps
python scripts/search_dev_universe.py -q "ai" -t roadmap

# Find Python AI agent libraries
python scripts/search_dev_universe.py -q "agent" -t library

# Find books on Rust
python scripts/search_dev_universe.py -q "rust" -t book
```

### Interactive REPL Shell
Launch an interactive search terminal:
```powershell
python scripts/search_dev_universe.py -i
```
Commands inside interactive mode:
- `saas:notion`: search open-source alternatives to Notion
- `type:self-hosted git`: find self-hosted Git repositories (Gitea, Forgejo, GitLab)
- `type:roadmap backend`: view backend developer roadmap
- `type:build-project redis`: find tutorials to build Redis from scratch
- `:stats`: display real-time database counts
- `:q`: quit

---

## 6. Web Dashboard (Zero-Dependency UI)

Open [`docs/dev_universe_explorer.html`](file:///e:/2027%20nov/docs/dev_universe_explorer.html) directly in any browser:
- **Instant client-side search** across all 10,189 resources.
- **Pill filters** by resource type (`Self-Hosted Apps`, `Roadmaps`, `Python Libraries`, `Books`, `Build Your Own`, `APIs`, `Courses`, etc.).
- **Category filtering** across 50+ primary domains.
- **Direct launch and copy links**.
- No web server required — loads instantly via `file://`.

---

## 7. SQLite Database & Direct SQL Queries

The SQLite database is located at [`data/dev_universe.db`](file:///e:/2027%20nov/data/dev_universe.db).

### Schema
```sql
CREATE TABLE resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    language TEXT,
    format TEXT,
    description TEXT,
    source_repo TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE resources_fts USING fts5(
    title, category, subcategory, description, type, source_repo,
    content='resources', content_rowid='id'
);
```

### Direct FTS5 Query Example (Python)
```python
import sqlite3
from pathlib import Path

db_uri = Path("data/dev_universe.db").resolve().as_uri()
conn = sqlite3.connect(f"{db_uri}?mode=ro", uri=True)
cursor = conn.cursor()

# Query self-hosted password managers with FTS5
cursor.execute("""
    SELECT r.title, r.type, r.category, r.url
    FROM resources r
    JOIN resources_fts fts ON r.id = fts.rowid
    WHERE r.type = 'self-hosted' AND resources_fts MATCH 'password*'
    LIMIT 5;
""")
for title, item_type, cat, url in cursor.fetchall():
    print(f"[{item_type}] {title} ({cat}) -> {url}")
conn.close()
```
