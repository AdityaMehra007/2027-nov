#!/usr/bin/env python3
"""
OmniDev Self-Hosted Launcher & Docker Compose Generator
Instantly generates production-grade Docker Compose stacks, environment secrets,
and reverse-proxy configs (Caddy) for top self-hosted applications.
"""

import sys
import os
import argparse
import secrets
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent

STACKS = {
    "nextcloud": {
        "name": "Nextcloud Hub",
        "category": "Cloud Storage & Collaboration",
        "replaces": "Google Drive, Dropbox, Microsoft 365",
        "port": 8080,
        "description": "Complete productivity platform with file sync, calendar, contacts, and collaborative office suite.",
        "compose": """version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-nextcloud}
      POSTGRES_USER: ${POSTGRES_USER:-nextcloud}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

  redis:
    image: redis:alpine
    restart: always

  app:
    image: nextcloud:apache
    restart: always
    ports:
      - "${PORT:-8080}:80"
    depends_on:
      - db
      - redis
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      POSTGRES_HOST: db
      POSTGRES_DB: ${POSTGRES_DB:-nextcloud}
      POSTGRES_USER: ${POSTGRES_USER:-nextcloud}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      REDIS_HOST: redis
      NEXTCLOUD_ADMIN_USER: ${ADMIN_USER:-admin}
      NEXTCLOUD_ADMIN_PASSWORD: ${ADMIN_PASSWORD}

volumes:
  db_data:
  nextcloud_data:
""",
        "env_defaults": {
            "POSTGRES_DB": "nextcloud",
            "POSTGRES_USER": "nextcloud",
            "POSTGRES_PASSWORD": lambda: secrets.token_hex(16),
            "ADMIN_USER": "admin",
            "ADMIN_PASSWORD": lambda: secrets.token_urlsafe(16),
            "PORT": "8080"
        }
    },

    "vaultwarden": {
        "name": "Vaultwarden",
        "category": "Password Management",
        "replaces": "1Password, Bitwarden Cloud, LastPass",
        "port": 8080,
        "description": "Lightweight Bitwarden-compatible password and secrets manager written in Rust.",
        "compose": """version: '3.8'

services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: always
    environment:
      WEBSOCKET_ENABLED: "true"
      SIGNUPS_ALLOWED: "${SIGNUPS_ALLOWED:-false}"
      ADMIN_TOKEN: "${ADMIN_TOKEN}"
    volumes:
      - vw_data:/data
    ports:
      - "${PORT:-8080}:80"

volumes:
  vw_data:
""",
        "env_defaults": {
            "SIGNUPS_ALLOWED": "true",
            "ADMIN_TOKEN": lambda: secrets.token_hex(32),
            "PORT": "8080"
        }
    },

    "uptime-kuma": {
        "name": "Uptime Kuma",
        "category": "Monitoring & Status Pages",
        "replaces": "StatusPage, Pingdom, Better Uptime",
        "port": 3001,
        "description": "Self-hosted monitoring tool with status pages, certificate checks, and 90+ notification services.",
        "compose": """version: '3.8'

services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: always
    volumes:
      - uptime_data:/app/data
    ports:
      - "${PORT:-3001}:3001"

volumes:
  uptime_data:
""",
        "env_defaults": {
            "PORT": "3001"
        }
    },

    "n8n": {
        "name": "n8n Workflow Automation",
        "category": "Automation & Integration",
        "replaces": "Zapier, Make (Integromat), Workato",
        "port": 5678,
        "description": "Fair-code workflow automation platform with native AI nodes, 400+ integrations, and custom JavaScript.",
        "compose": """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER:-n8n}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME:-n8n}
    volumes:
      - n8n_db_data:/var/lib/postgresql/data

  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    ports:
      - "${PORT:-5678}:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${DB_NAME:-n8n}
      - DB_POSTGRESDB_USER=${DB_USER:-n8n}
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

volumes:
  n8n_db_data:
  n8n_data:
""",
        "env_defaults": {
            "DB_USER": "n8n",
            "DB_PASSWORD": lambda: secrets.token_hex(16),
            "DB_NAME": "n8n",
            "N8N_ENCRYPTION_KEY": lambda: secrets.token_hex(32),
            "PORT": "5678"
        }
    },

    "umami": {
        "name": "Umami Analytics",
        "category": "Analytics",
        "replaces": "Google Analytics, Plausible",
        "port": 3000,
        "description": "Privacy-focused, cookie-free open-source alternative to Google Analytics with lightweight script.",
        "compose": """version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-umami}
      POSTGRES_USER: ${POSTGRES_USER:-umami}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - umami_db:/var/lib/postgresql/data

  umami:
    image: ghcr.io/umami-software/umami:postgresql-latest
    restart: always
    ports:
      - "${PORT:-3000}:3000"
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER:-umami}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB:-umami}
      APP_SECRET: ${APP_SECRET}
    depends_on:
      - db

volumes:
  umami_db:
""",
        "env_defaults": {
            "POSTGRES_DB": "umami",
            "POSTGRES_USER": "umami",
            "POSTGRES_PASSWORD": lambda: secrets.token_hex(16),
            "APP_SECRET": lambda: secrets.token_hex(32),
            "PORT": "3000"
        }
    },

    "appflowy": {
        "name": "AppFlowy",
        "category": "Task Management & Notes",
        "replaces": "Notion, Coda",
        "port": 8000,
        "description": "Open-source Notion alternative with offline-first data ownership, boards, calendars, and rich documents.",
        "compose": """version: '3.8'

services:
  appflowy_cloud:
    image: appflowyinc/appflowy_cloud:latest
    restart: always
    ports:
      - "${PORT:-8000}:8000"
    environment:
      APPFLOWY_DATABASE_URL: postgres://${DB_USER:-appflowy}:${DB_PASSWORD}@postgres:5432/${DB_NAME:-appflowy}
      GOTRUE_JWT_SECRET: ${JWT_SECRET}
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER:-appflowy}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME:-appflowy}
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    restart: always

volumes:
  pgdata:
""",
        "env_defaults": {
            "DB_USER": "appflowy",
            "DB_PASSWORD": lambda: secrets.token_hex(16),
            "DB_NAME": "appflowy",
            "JWT_SECRET": lambda: secrets.token_hex(32),
            "PORT": "8000"
        }
    },

    "gitea": {
        "name": "Gitea",
        "category": "Code Hosting & CI/CD",
        "replaces": "GitHub, GitLab",
        "port": 3000,
        "description": "Ultra-fast, lightweight Git service written in Go with built-in CI/CD Actions and package registry.",
        "compose": """version: '3.8'

services:
  server:
    image: gitea/gitea:latest
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=postgres
      - GITEA__database__HOST=db:5432
      - GITEA__database__NAME=${DB_NAME:-gitea}
      - GITEA__database__USER=${DB_USER:-gitea}
      - GITEA__database__PASSWD=${DB_PASSWORD}
    restart: always
    volumes:
      - gitea_data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "${PORT:-3000}:3000"
      - "${SSH_PORT:-2222}:22"
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_USER=${DB_USER:-gitea}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-gitea}
    volumes:
      - gitea_db:/var/lib/postgresql/data

volumes:
  gitea_data:
  gitea_db:
""",
        "env_defaults": {
            "DB_USER": "gitea",
            "DB_PASSWORD": lambda: secrets.token_hex(16),
            "DB_NAME": "gitea",
            "PORT": "3000",
            "SSH_PORT": "2222"
        }
    },

    "paperless-ngx": {
        "name": "Paperless-ngx",
        "category": "Document Management",
        "replaces": "Adobe Acrobat, DocuWare, Google Drive Scan",
        "port": 8000,
        "description": "Document management system with automatic OCR, tagging, search, and indexing for receipts and PDFs.",
        "compose": """version: '3.8'

services:
  broker:
    image: redis:7-alpine
    restart: always

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    restart: always
    depends_on:
      - broker
    ports:
      - "${PORT:-8000}:8000"
    environment:
      PAPERLESS_REDIS: redis://broker:6379
      PAPERLESS_SECRET_KEY: ${SECRET_KEY}
      PAPERLESS_ADMIN_USER: ${ADMIN_USER:-admin}
      PAPERLESS_ADMIN_PASSWORD: ${ADMIN_PASSWORD}
    volumes:
      - paperless_data:/usr/src/paperless/data
      - paperless_media:/usr/src/paperless/media
      - paperless_export:/usr/src/paperless/export
      - ./consume:/usr/src/paperless/consume

volumes:
  paperless_data:
  paperless_media:
  paperless_export:
""",
        "env_defaults": {
            "SECRET_KEY": lambda: secrets.token_hex(32),
            "ADMIN_USER": "admin",
            "ADMIN_PASSWORD": lambda: secrets.token_urlsafe(16),
            "PORT": "8000"
        }
    },

    "ghost": {
        "name": "Ghost",
        "category": "Publishing & Newsletters",
        "replaces": "Substack, Medium, WordPress",
        "port": 2368,
        "description": "Modern publishing platform for newsletters, memberships, and premium subscription publications.",
        "compose": """version: '3.8'

services:
  ghost:
    image: ghost:5-alpine
    restart: always
    ports:
      - "${PORT:-2368}:2368"
    environment:
      database__client: mysql
      database__connection__host: db
      database__connection__user: ${DB_USER:-ghost}
      database__connection__password: ${DB_PASSWORD}
      database__connection__database: ${DB_NAME:-ghost}
      url: ${URL:-http://localhost:2368}
    volumes:
      - ghost_content:/var/lib/ghost/content
    depends_on:
      - db

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME:-ghost}
      MYSQL_USER: ${DB_USER:-ghost}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ghost_mysql:/var/lib/mysql

volumes:
  ghost_content:
  ghost_mysql:
""",
        "env_defaults": {
            "DB_USER": "ghost",
            "DB_PASSWORD": lambda: secrets.token_hex(16),
            "ROOT_PASSWORD": lambda: secrets.token_hex(20),
            "DB_NAME": "ghost",
            "URL": "http://localhost:2368",
            "PORT": "2368"
        }
    },

    "meilisearch": {
        "name": "Meilisearch",
        "category": "Search Engines",
        "replaces": "Algolia, Elasticsearch",
        "port": 7700,
        "description": "Lightning-fast, typo-tolerant search engine with instant search-as-you-type responses.",
        "compose": """version: '3.8'

services:
  meilisearch:
    image: getmeili/meilisearch:v1.6
    restart: always
    ports:
      - "${PORT:-7700}:7700"
    environment:
      MEILI_MASTER_KEY: ${MEILI_MASTER_KEY}
      MEILI_ENV: production
    volumes:
      - meili_data:/meili_data

volumes:
  meili_data:
""",
        "env_defaults": {
            "MEILI_MASTER_KEY": lambda: secrets.token_hex(24),
            "PORT": "7700"
        }
    }
}

def list_stacks():
    print("=" * 80)
    print("  🚀 OMNIDEV UNIVERSE: SELF-HOSTED PRODUCTION DOCKER STACKS")
    print("=" * 80)
    print(f"{'Stack Key':<15} {'Application Name':<22} {'Replaces (SaaS)':<30} {'Default Port'}")
    print("-" * 80)
    for key, s in sorted(STACKS.items()):
        print(f"{key:<15} {s['name']:<22} {s['replaces']:<30} :{s['port']}")
    print("-" * 80)
    print("To inspect:  python scripts/selfhosted_launcher.py info <stack-key>")
    print("To generate: python scripts/selfhosted_launcher.py generate <stack-key> --output ./deploy/<stack-key>")
    print()

def show_info(app_key: str):
    if app_key not in STACKS:
        print(f"Error: Unknown stack '{app_key}'. Available: {', '.join(STACKS.keys())}")
        sys.exit(1)
    s = STACKS[app_key]
    print(f"\n📦 Stack: {s['name']} ({app_key})")
    print(f"Category : {s['category']}")
    print(f"Replaces : {s['replaces']}")
    print(f"Port     : {s['port']}")
    print(f"Summary  : {s['description']}\n")
    print("Default Environment Variables generated:")
    for k, v in s["env_defaults"].items():
        val_sample = "<auto-generated secure secret>" if callable(v) else v
        print(f"  - {k} = {val_sample}")
    print()

def generate_stack(app_key: str, output_dir: Path, domain: str = None, with_caddy: bool = False):
    if app_key not in STACKS:
        print(f"Error: Unknown stack '{app_key}'. Available: {', '.join(STACKS.keys())}")
        sys.exit(1)

    s = STACKS[app_key]
    output_dir.mkdir(parents=True, exist_ok=True)

    compose_file = output_dir / "docker-compose.yml"
    env_file = output_dir / ".env"

    # Generate environment variables
    env_lines = [f"# Automated Environment Config for {s['name']}", f"# Generated by OmniDev Self-Hosted Launcher\n"]
    for k, v in s["env_defaults"].items():
        val = v() if callable(v) else v
        env_lines.append(f"{k}={val}")

    with open(env_file, "w", encoding="utf-8") as f:
        f.write("\n".join(env_lines) + "\n")

    with open(compose_file, "w", encoding="utf-8") as f:
        f.write(s["compose"])

    print(f"✅ Generated {s['name']} stack in: {output_dir}")
    print(f"   • docker-compose.yml written")
    print(f"   • .env written with cryptographically secure random credentials")

    if with_caddy:
        target_domain = domain or f"{app_key}.local"
        caddyfile = output_dir / "Caddyfile"
        caddy_content = f"""{target_domain} {{
    reverse_proxy localhost:{s['port']}
}}
"""
        with open(caddyfile, "w", encoding="utf-8") as f:
            f.write(caddy_content)
        print(f"   • Caddyfile written for automatic HTTPS on: {target_domain}")

    print("\nTo deploy this stack:")
    print(f"   cd {output_dir}")
    print("   docker compose up -d\n")

def main():
    parser = argparse.ArgumentParser(description="OmniDev Self-Hosted Stack Generator")
    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="List all supported self-hosted applications")

    # info
    info_p = subparsers.add_parser("info", help="Show application specs and parameters")
    info_p.add_argument("app", help="Application key (e.g. nextcloud, vaultwarden, umami, n8n)")

    # generate
    gen_p = subparsers.add_parser("generate", help="Generate production-ready compose stack")
    gen_p.add_argument("app", help="Application key (e.g. nextcloud, vaultwarden, umami, n8n)")
    gen_p.add_argument("-o", "--output", default=None, help="Target directory (default: deploy/<app>)")
    gen_p.add_argument("-d", "--domain", default=None, help="Domain name for Caddyfile reverse proxy")
    gen_p.add_argument("--with-caddy", action="store_true", help="Generate Caddy reverse-proxy config with automated SSL")

    args = parser.parse_args()

    if args.command == "list" or not args.command:
        list_stacks()
    elif args.command == "info":
        show_info(args.app)
    elif args.command == "generate":
        out = Path(args.output) if args.output else BASE_DIR / "deploy" / "selfhosted" / args.app
        generate_stack(args.app, out, domain=args.domain, with_caddy=args.with_caddy)

if __name__ == "__main__":
    main()
