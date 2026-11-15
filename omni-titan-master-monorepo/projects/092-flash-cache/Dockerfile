FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_092_flash_cache

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_092_flash_cache /app/omni_092_flash_cache
USER nonroot:nonroot
EXPOSE 9092
ENTRYPOINT ["/app/omni_092_flash_cache"]
