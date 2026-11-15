FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_111_topological_qpu_code

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_111_topological_qpu_code /app/omni_111_topological_qpu_code
USER nonroot:nonroot
EXPOSE 9111
ENTRYPOINT ["/app/omni_111_topological_qpu_code"]
