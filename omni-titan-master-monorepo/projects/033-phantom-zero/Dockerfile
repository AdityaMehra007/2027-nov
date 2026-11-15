FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_033_phantom_zero

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_033_phantom_zero /app/omni_033_phantom_zero
USER nonroot:nonroot
EXPOSE 9033
ENTRYPOINT ["/app/omni_033_phantom_zero"]
