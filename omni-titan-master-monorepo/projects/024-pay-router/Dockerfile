FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_024_pay_router

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_024_pay_router /app/omni_024_pay_router
USER nonroot:nonroot
EXPOSE 9024
ENTRYPOINT ["/app/omni_024_pay_router"]
