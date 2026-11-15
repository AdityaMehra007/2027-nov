FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_063_sync_pipe

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_063_sync_pipe /app/omni_063_sync_pipe
USER nonroot:nonroot
EXPOSE 9063
ENTRYPOINT ["/app/omni_063_sync_pipe"]
