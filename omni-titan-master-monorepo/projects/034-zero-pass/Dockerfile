FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_034_zero_pass

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_034_zero_pass /app/omni_034_zero_pass
USER nonroot:nonroot
EXPOSE 9034
ENTRYPOINT ["/app/omni_034_zero_pass"]
