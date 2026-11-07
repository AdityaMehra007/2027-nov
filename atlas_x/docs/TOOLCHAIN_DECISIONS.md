# Toolchain decisions and compatibility notes

| Layer | Choice | Rationale | Current validation status |
|---|---|---|---|
| Control plane | Go | Strong stdlib networking, concurrency and deployment simplicity | Compiled/tested with Go 1.23.2 |
| Policy reference | Rust 2024 | Memory safety and explicit capability checks | Source created; not compiled here because rustc/cargo unavailable |
| AI baseline | Python | Ecosystem fit for evaluation and model integration | Tested with Python 3.13.5 |
| SDK/console | TypeScript | Typed browser and developer interfaces | Type-checked with installed TypeScript 5.8.3 |
| Data contract | SQL/PostgreSQL | Transactional relational state and workspace boundaries | Migration supplied; not applied to a live database |
| Formal model | TLA+ sketch | State-transition safety properties | Source supplied; not model-checked here |

Do not pin to a pre-release compiler solely for novelty. Adopt stable, supported toolchains and update versions through tested dependency changes. The TypeScript SDK is compiled against locally available TypeScript 5.8.3; TypeScript 7.x may be evaluated separately after stable compatibility is confirmed.
