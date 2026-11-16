# 10. Company Discovery System
**Project:** PROJECT ONE // Ingestion & Deduplication Pipeline  
**Date:** 2026-11-16  

## Deduplication & Verification Pipeline
1. Ingest raw public domain / entity name.
2. Normalize domain (strip http/https/www/trailing slashes).
3. Primary key collision check against `CompanyIntelligenceRegistry`.
4. Confidence scoring (0.0 to 1.0) based on verified website, LinkedIn presence, and legal registration.
5. Ingest buying signals and operational pain indicators into SQLite FTS5 database.
