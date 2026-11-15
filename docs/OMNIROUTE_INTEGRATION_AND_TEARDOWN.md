# OmniRoute Architectural Teardown & OmniVerse Native Integration Specification

## 1. Executive Summary

**OmniRoute** (by `cheaper-inference`) is an open-source, MIT-licensed AI Gateway and cost-optimization proxy. Its central mission is to aggregate heterogeneous LLM providers (from cloud hyperscalers like OpenAI, Anthropic, and Google Gemini to low-cost and open-weight providers like DeepSeek, Groq, Mistral, and local Ollama) behind a unified, OpenAI-compatible endpoint.

In **CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC**, high-frequency agent swarms (`OmniSwarm Mesh`, B2B agency crawlers, automated code generators, financial risk models) incur substantial token expenses and encounter upstream rate limits (HTTP 429). Integrating OmniRoute principles directly into the zero-dependency `PyControlPlane` fabric (`src/pycontrolplane/ai_gateway/`) establishes a sovereign, self-healing, cost-minimizing inference gateway for the entire repository.

---

## 2. OmniRoute Core Architecture & Teardown

```
                          ┌────────────────────────┐
                          │   Agent / SDK Client   │
                          │ (OpenAI SDK, Cursor,   │
                          │  Claude Code, Codex)   │
                          └───────────┬────────────┘
                                      │ HTTP /v1/chat/completions
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │       OmniRoute Gateway Core (Port 4000)         │
             │                                                  │
             │  ┌────────────────────────────────────────────┐  │
             │  │ 1. Guardrail & Quota Firewall              │  │
             │  │    - Prompt injection detection            │  │
             │  │    - PII scrubbing (SSN, Email, CC)        │  │
             │  │    - Tenant token bucket limit             │  │
             │  └─────────────────────┬──────────────────────┘  │
             │                        ▼                         │
             │  ┌────────────────────────────────────────────┐  │
             │  │ 2. Context / Token Compressor (RTK/Caveman)│  │
             │  │    - Preamble/postamble stripping          │  │
             │  │    - Whitespace & indentation pruning      │  │
             │  │    - Filler phrase reduction               │  │
             │  │    - 20-40% input token savings            │  │
             │  └─────────────────────┬──────────────────────┘  │
             │                        ▼                         │
             │  ┌────────────────────────────────────────────┐  │
             │  │ 3. Semantic & Exact Hash Cache             │  │
             │  │    - O(1) Exact SHA-256 match              │  │
             │  │    - Cosine vector similarity (sim >= 0.90)│  │
             │  └──────────┬─────────────────────────┬───────┘  │
             │     Cache Hit (0 cost)          Cache Miss       │
             │             │                         ▼          │
             │             │            ┌────────────────────┐  │
             │             │            │ 4. Dynamic Router  │  │
             │             │            │    & Fallback Mesh │  │
             │             │            └─────────┬──────────┘  │
             └─────────────┼──────────────────────┼─────────────┘
                           │                      │
           Return Cached ──┘                      │ Cascading Upstream
                                                  ▼
     ┌────────────────────────────────────────────────────────────────────────┐
     │ Upstream Provider Endpoints (Dispatched by Tier & Cost)                │
     │  - Tier 0: LOCAL/EDGE   -> Ollama, PyTransformer (Free, 0ms network)   │
     │  - Tier 1: BUDGET/FAST  -> DeepSeek Chat, Groq Llama, Gemini Flash     │
     │  - Tier 2: REASONING    -> Claude 3.5 Sonnet, GPT-4o, DeepSeek-R1      │
     │                                                                        │
     │  * Automatic Failover: On HTTP 429 (Rate Limit) or 5xx, trips breaker  │
     │    and falls back to next provider in tier with zero caller failure.   │
     └────────────────────────────────────────────────────────────────────────┘
```

### Key Pillars of OmniRoute

1. **Universal Protocol Normalization**:
   - Exposes standard OpenAI REST endpoints (`/v1/chat/completions`, `/v1/models`, `/v1/embeddings`).
   - Translates OpenAI-style payloads to provider-specific formats (e.g., Anthropic Messages API, Gemini generateContent, Groq OpenAI-format).

2. **Token Compression (Caveman & RTK)**:
   - Eliminates politeness boilerplate ("Hello, please provide...", "Thank you in advance").
   - Strips redundant markdown separators and multiple consecutive blank lines.
   - Preserves code syntax, brackets, JSON structures, and technical identifiers.
   - Provides measurable token savings metrics (e.g. 15%-35% reduction in prompt tokens).

3. **Quota-Aware Dynamic Routing**:
   - Maintains continuous provider telemetry: latency ($p50/p95$), error rates, and 429 status cooldown timers.
   - Automatic routing based on prompt intent (heuristics detect reasoning keywords: "prove", "step-by-step", "architect", "formalize").
   - Cascading fallback: If Groq or DeepSeek hits a rate limit, the router silently redirects the request to Gemini Flash or Local Edge without throwing an error to the calling agent.

4. **Self-Healing Circuit Breaker**:
   - Each endpoint is governed by a 3-state Circuit Breaker (`CLOSED`, `OPEN`, `HALF_OPEN`).
   - Prevents cascading gateway stalls when an external provider experiences degraded performance or outage.

---

## 3. OmniVerse Native Integration Plan

Rather than forcing the OmniVerse operating system to rely exclusively on an external Node/Docker service, we implement a **dual-surface bridge**:

1. **Full Submodule / Directory Ingestion (`OmniRoute/`)**:
   - Cloned directly into the root workspace for standalone Node/Docker deployments and upstream updates.
   - Controlled via `scripts/omniroute_bridge.py`.

2. **Native Zero-Dependency Python Bridge (`src/pycontrolplane/ai_gateway/`)**:
   - Zero external pip dependencies; runs directly in Python 3.13 stdlib.
   - Modules added:
     - `src/pycontrolplane/ai_gateway/compressor.py`: Pure-Python RTK/Caveman token compressor.
     - `src/pycontrolplane/ai_gateway/omniroute_engine.py`: Multi-provider catalog, quota tracker, and intelligent tiered router.
     - `src/pycontrolplane/ai_gateway/gateway_server.py`: Standard library `http.server` providing the OpenAI `/v1/chat/completions` and `/v1/models` HTTP gateway.
     - `scripts/omniroute_bridge.py`: CLI supervisor to launch, monitor, or route through either the native Python gateway or the Node OmniRoute server.

---

## 4. Specification: Compression & Routing Rules

### Compression Modes
- `PASSTHROUGH`: No modification.
- `LIGHT`: Strips duplicate whitespace, trailing spaces, and redundant empty lines.
- `CAVEMAN`: Light + strips conversational conversational filler words ("please", "kindly", "could you", "in order to", "would appreciate"), and optimizes prompt conciseness.
- `AGGRESSIVE`: Caveman + collapses non-code multi-line sentences to dense semantic fragments.

### Quota Cooldown Policy
- On HTTP `429` or `quota_exceeded`: Provider endpoint enters `COOLDOWN` for 60 seconds.
- Router immediately routes to the next healthiest provider with matching capability.
- When cooldown expires, router sends a single probe request (`HALF_OPEN`) to confirm recovery.

---

## 5. Verification & Compliance
- Complies with `GLOSSARY.md` (Autonomous Tasks vs. Gated Operations).
- Strict adherence to TDD: Unit and integration tests in `tests/test_omniroute_bridge.py`.
- 100% test pass rate verified through `pytest`.
