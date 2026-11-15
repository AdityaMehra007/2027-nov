FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_103_quantum_vault_lwe_stark

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_103_quantum_vault_lwe_stark /app/omni_103_quantum_vault_lwe_stark
USER nonroot:nonroot
EXPOSE 9103
ENTRYPOINT ["/app/omni_103_quantum_vault_lwe_stark"]
