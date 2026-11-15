FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_039_crypt_enclave

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_039_crypt_enclave /app/omni_039_crypt_enclave
USER nonroot:nonroot
EXPOSE 9039
ENTRYPOINT ["/app/omni_039_crypt_enclave"]
