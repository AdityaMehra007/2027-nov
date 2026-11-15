FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_097_sync_core

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_097_sync_core /app/omni_097_sync_core
USER nonroot:nonroot
EXPOSE 9097
ENTRYPOINT ["/app/omni_097_sync_core"]
