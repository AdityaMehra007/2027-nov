FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_016_kube_autopilot

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_016_kube_autopilot /app/omni_016_kube_autopilot
USER nonroot:nonroot
EXPOSE 9016
ENTRYPOINT ["/app/omni_016_kube_autopilot"]
