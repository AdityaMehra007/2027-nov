FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_095_aether_lang

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_095_aether_lang /app/omni_095_aether_lang
USER nonroot:nonroot
EXPOSE 9095
ENTRYPOINT ["/app/omni_095_aether_lang"]
