FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_005_veritas_ai

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_005_veritas_ai /app/omni_005_veritas_ai
USER nonroot:nonroot
EXPOSE 9005
ENTRYPOINT ["/app/omni_005_veritas_ai"]
