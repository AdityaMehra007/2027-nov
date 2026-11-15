FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_077_sonic_studio

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_077_sonic_studio /app/omni_077_sonic_studio
USER nonroot:nonroot
EXPOSE 9077
ENTRYPOINT ["/app/omni_077_sonic_studio"]
