FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_037_code_fortress

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_037_code_fortress /app/omni_037_code_fortress
USER nonroot:nonroot
EXPOSE 9037
ENTRYPOINT ["/app/omni_037_code_fortress"]
