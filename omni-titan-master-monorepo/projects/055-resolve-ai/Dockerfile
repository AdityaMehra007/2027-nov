FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_055_resolve_ai

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_055_resolve_ai /app/omni_055_resolve_ai
USER nonroot:nonroot
EXPOSE 9055
ENTRYPOINT ["/app/omni_055_resolve_ai"]
