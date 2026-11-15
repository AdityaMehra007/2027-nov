FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_098_quantum_sim

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_098_quantum_sim /app/omni_098_quantum_sim
USER nonroot:nonroot
EXPOSE 9098
ENTRYPOINT ["/app/omni_098_quantum_sim"]
