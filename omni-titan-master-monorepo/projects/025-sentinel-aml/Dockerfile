FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_025_sentinel_aml

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_025_sentinel_aml /app/omni_025_sentinel_aml
USER nonroot:nonroot
EXPOSE 9025
ENTRYPOINT ["/app/omni_025_sentinel_aml"]
