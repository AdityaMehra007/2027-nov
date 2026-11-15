FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_064_metric_canvas

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_064_metric_canvas /app/omni_064_metric_canvas
USER nonroot:nonroot
EXPOSE 9064
ENTRYPOINT ["/app/omni_064_metric_canvas"]
