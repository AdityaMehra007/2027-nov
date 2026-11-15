FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_013_edge_vortex

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_013_edge_vortex /app/omni_013_edge_vortex
USER nonroot:nonroot
EXPOSE 9013
ENTRYPOINT ["/app/omni_013_edge_vortex"]
