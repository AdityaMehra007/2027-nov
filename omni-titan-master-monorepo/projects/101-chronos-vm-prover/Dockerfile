FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_101_chronos_vm_prover

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_101_chronos_vm_prover /app/omni_101_chronos_vm_prover
USER nonroot:nonroot
EXPOSE 9101
ENTRYPOINT ["/app/omni_101_chronos_vm_prover"]
