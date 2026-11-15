FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_018_chaos_shield

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_018_chaos_shield /app/omni_018_chaos_shield
USER nonroot:nonroot
EXPOSE 9018
ENTRYPOINT ["/app/omni_018_chaos_shield"]
