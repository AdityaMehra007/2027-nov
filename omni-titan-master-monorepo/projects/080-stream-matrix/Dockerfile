FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_080_stream_matrix

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_080_stream_matrix /app/omni_080_stream_matrix
USER nonroot:nonroot
EXPOSE 9080
ENTRYPOINT ["/app/omni_080_stream_matrix"]
