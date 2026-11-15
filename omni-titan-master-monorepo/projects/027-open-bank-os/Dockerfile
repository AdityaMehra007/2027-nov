FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_027_open_bank_os

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_027_open_bank_os /app/omni_027_open_bank_os
USER nonroot:nonroot
EXPOSE 9027
ENTRYPOINT ["/app/omni_027_open_bank_os"]
