FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_032_cloud_graph_sec

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_032_cloud_graph_sec /app/omni_032_cloud_graph_sec
USER nonroot:nonroot
EXPOSE 9032
ENTRYPOINT ["/app/omni_032_cloud_graph_sec"]
