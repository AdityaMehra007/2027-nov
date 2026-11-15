FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_001_aether_os

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_001_aether_os /app/omni_001_aether_os
USER nonroot:nonroot
EXPOSE 9001
ENTRYPOINT ["/app/omni_001_aether_os"]
