# 26. Deployment Instructions
**Project:** PROJECT ONE // Multi-Cloud Infrastructure  
**Date:** 2026-11-16  

## Deployment Surfaces
1. **Local Bare Metal (Workstation):** Run FastAPI on `127.0.0.1:8888` with background daemons.
2. **Cloudflare Workers / Pages:** Edge proxying of static assets and telemetry routing.
3. **Render / Fly.io Container:** Dockerfile deployment with persistent volume mount for SQLite FTS5 database.
