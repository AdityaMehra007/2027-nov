FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_004_cortex_graph

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_004_cortex_graph /app/omni_004_cortex_graph
USER nonroot:nonroot
EXPOSE 9004
ENTRYPOINT ["/app/omni_004_cortex_graph"]
