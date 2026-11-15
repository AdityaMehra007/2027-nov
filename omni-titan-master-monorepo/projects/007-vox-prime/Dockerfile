FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_007_vox_prime

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_007_vox_prime /app/omni_007_vox_prime
USER nonroot:nonroot
EXPOSE 9007
ENTRYPOINT ["/app/omni_007_vox_prime"]
