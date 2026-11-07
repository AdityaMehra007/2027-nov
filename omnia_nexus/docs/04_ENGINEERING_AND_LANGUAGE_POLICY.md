# Engineering and Language Policy

| Domain | Candidate technologies | Use only when |
|---|---|---|
| Systems safety | Rust, C | Memory safety, low-level control or measured performance requires it |
| Control plane | Go, Java, Rust | Concurrency, service ownership and operational needs justify it |
| AI and research | Python, PyTorch, JAX | Model/research ecosystem is needed |
| Product and SDK | TypeScript, React | Web UX and typed interfaces are required |
| Data integrity | SQL, PostgreSQL | Transactions, relational constraints and analytics are required |
| Compute acceleration | C++, CUDA, HIP | Profiling identifies accelerator benefit and hardware exists |
| Hardware logic | SystemVerilog, VHDL | An actual chip/FPGA programme is approved |
| Numerical science | Julia, Python, MATLAB | Domain libraries, reproducibility and performance fit |
| Mobile/edge | Swift, Kotlin, C/C++ | Native or embedded needs justify |
| Plugin execution | WebAssembly/WASI | Untrusted portable extensions are required |
| Formal methods | TLA+, Alloy, Lean, Coq | Critical protocol/state invariants merit formal analysis |
| Infrastructure | Terraform, Bash, Go, YAML | Reproducible operations are required |

## Engineering rules
- Modular monolith first.
- Domain boundaries before service boundaries.
- Explicit schemas and versioned contracts.
- Type safety and input validation.
- Secure defaults and least privilege.
- Reproducible builds and dependency pinning.
- SBOM and licence review.
- Unit, integration, property and end-to-end tests where relevant.
- Benchmarks before optimisation.
- Threat model before external exposure.
- Backups and recovery before production.
- No "production-ready" claim without operational evidence.

## Research vs production
A research branch may use experimental frameworks. Production must use supported versions, maintained dependencies, reproducible builds, monitoring, security review and a migration plan.
