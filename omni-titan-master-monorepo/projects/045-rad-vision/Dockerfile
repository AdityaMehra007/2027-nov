FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_045_rad_vision

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_045_rad_vision /app/omni_045_rad_vision
USER nonroot:nonroot
EXPOSE 9045
ENTRYPOINT ["/app/omni_045_rad_vision"]
