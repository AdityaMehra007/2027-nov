FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_062_warp_stream_x

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_062_warp_stream_x /app/omni_062_warp_stream_x
USER nonroot:nonroot
EXPOSE 9062
ENTRYPOINT ["/app/omni_062_warp_stream_x"]
