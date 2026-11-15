FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_070_click_stream_pro

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_070_click_stream_pro /app/omni_070_click_stream_pro
USER nonroot:nonroot
EXPOSE 9070
ENTRYPOINT ["/app/omni_070_click_stream_pro"]
