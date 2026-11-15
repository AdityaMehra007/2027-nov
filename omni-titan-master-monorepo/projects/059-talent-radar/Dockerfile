FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_059_talent_radar

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_059_talent_radar /app/omni_059_talent_radar
USER nonroot:nonroot
EXPOSE 9059
ENTRYPOINT ["/app/omni_059_talent_radar"]
