FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_096_quorum_queue

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_096_quorum_queue /app/omni_096_quorum_queue
USER nonroot:nonroot
EXPOSE 9096
ENTRYPOINT ["/app/omni_096_quorum_queue"]
