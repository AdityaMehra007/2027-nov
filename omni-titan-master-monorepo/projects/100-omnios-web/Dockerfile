FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_100_omnios_web

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_100_omnios_web /app/omni_100_omnios_web
USER nonroot:nonroot
EXPOSE 9100
ENTRYPOINT ["/app/omni_100_omnios_web"]
