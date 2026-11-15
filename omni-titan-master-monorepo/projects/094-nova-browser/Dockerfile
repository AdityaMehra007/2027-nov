FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_094_nova_browser

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_094_nova_browser /app/omni_094_nova_browser
USER nonroot:nonroot
EXPOSE 9094
ENTRYPOINT ["/app/omni_094_nova_browser"]
