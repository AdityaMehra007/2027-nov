FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_086_sky_command

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_086_sky_command /app/omni_086_sky_command
USER nonroot:nonroot
EXPOSE 9086
ENTRYPOINT ["/app/omni_086_sky_command"]
