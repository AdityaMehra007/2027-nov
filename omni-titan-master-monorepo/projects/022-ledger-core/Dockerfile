FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_022_ledger_core

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_022_ledger_core /app/omni_022_ledger_core
USER nonroot:nonroot
EXPOSE 9022
ENTRYPOINT ["/app/omni_022_ledger_core"]
