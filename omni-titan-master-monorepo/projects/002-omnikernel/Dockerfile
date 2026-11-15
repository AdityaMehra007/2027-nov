FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_002_omnikernel

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_002_omnikernel /app/omni_002_omnikernel
USER nonroot:nonroot
EXPOSE 9002
ENTRYPOINT ["/app/omni_002_omnikernel"]
