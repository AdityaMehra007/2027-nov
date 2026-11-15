FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_038_dark_watch

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_038_dark_watch /app/omni_038_dark_watch
USER nonroot:nonroot
EXPOSE 9038
ENTRYPOINT ["/app/omni_038_dark_watch"]
