FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_009_epoch_eval

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_009_epoch_eval /app/omni_009_epoch_eval
USER nonroot:nonroot
EXPOSE 9009
ENTRYPOINT ["/app/omni_009_epoch_eval"]
