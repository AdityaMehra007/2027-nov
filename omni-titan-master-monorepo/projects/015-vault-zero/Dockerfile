FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_015_vault_zero

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_015_vault_zero /app/omni_015_vault_zero
USER nonroot:nonroot
EXPOSE 9015
ENTRYPOINT ["/app/omni_015_vault_zero"]
